#include "syscall.h"
#include "copyright.h"

int main()
{
	int is_Success;
	SpaceId id_Input, id_Output, id_SV, id_Res;
	int n = 0, i = 0;
	char c_ReadFile;

	if (CreateSemaphore("main", 0) == -1)
		return 1;

	if (CreateSemaphore("sinhvien", 0) == -1)
		return 1;

	if (CreateSemaphore("voinuoc", 0) == -1)
		return 1;

	if (CreateSemaphore("m_vn", 0) == -1)
		return 1;

	if (CreateFile("output.txt") == -1)
		return 1;

	id_Input = Open("input.txt", 1);
	if (id_Input == -1)
		return 1;

	id_Output = Open("output.txt", 0);

	if (id_Output == -1)
	{
		Close(id_Input);
		return 1;
	}

	while (1)
	{
		Read(&c_ReadFile, 1, id_Input);
		if (c_ReadFile != '\n')
		{
			if (c_ReadFile >= '0' && c_ReadFile <= '9')
				n = n * 10 + (c_ReadFile - '0');
		}
		else
			break;
	}

	if (Exec("./test/sinhvien") == -1)
	{
		Close(id_Input);
		Close(id_Output);
		return 1;
	}

	if (Exec("./test/voinuoc") == -1)
	{
		Close(id_Input);
		Close(id_Output);
		return 1;
	}

	for (i; i < n; i++)
	{
		if (CreateFile("sinhvien.txt") == -1)
		{
			Close(id_Input);
			Close(id_Output);
			return 1;
		}

		id_SV = Open("sinhvien.txt", 0);
		if (id_SV == -1)
		{
			Close(id_Input);
			Close(id_Output);
			return 1;
		}

		while (1)
		{
			if (Read(&c_ReadFile, 1, id_Input) < 1)
			{
				break;
			}

			if (c_ReadFile != '\n')
			{
				Write(&c_ReadFile, 1, id_SV);
			}
			else
				break;
		}
		// Dong file sinhvien.txt lai
		Close(id_SV);

		// Goi tien trinh sinhvien hoat dong
		Up("sinhvien");

		// Tien trinh chinh phai cho
		Down("main");

		// Thuc hien doc file tu result va ghi vao ket qua o output.txt
		id_Res = Open("result.txt", 1);
		if (id_Res == -1)
		{
			Close(id_Input);
			Close(id_Output);
			return 1;
		}

		// Doc cac voi vao output.txt
		while (1)
		{
			if (Read(&c_ReadFile, 1, id_Res) < 1)
			{
				Write("\r\n", 2, id_Output);
				Close(id_Res);
				Up("m_vn");
				break;
			}
			Write(&c_ReadFile, 1, id_Output);
		}
	}

	Close(id_Input);
	Close(id_Output);
	Halt();
	return 0;
}
