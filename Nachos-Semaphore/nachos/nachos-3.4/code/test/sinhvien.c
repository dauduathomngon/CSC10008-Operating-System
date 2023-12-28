#include "syscall.h"
#include "copyright.h"

void main()
{
	// Khai bao
	SpaceId id_SV, id_Voinuoc;
	char temp;
	int flag_VN;
	int flag_MAIN;
	int fileSize;
	int p_File;
	//-----------------------------------------------------------
	Up("end");

	while (1)
	{
		fileSize = 0;

		Down("sinhvien");

		if (CreateFile("result.txt") == -1)
		{
			Up("main"); // tro ve tien trinh chinh
			return;
		}

		// Mo file sinhvien.txt len de doc
		id_SV = Open("sinhvien.txt", 1);
		if (id_SV == -1)
		{
			Up("main"); // tro ve tien trinh chinh
			return;
		}

		fileSize = Seek(-1, id_SV);
		Seek(0, id_SV);
		p_File = 0;

		// Tao file voinuoc.txt
		if (CreateFile("voinuoc.txt") == -1)
		{
			Close(id_SV);
			Up("main"); // tro ve tien trinh chinh
			return;
		}

		// Mo file voinuoc.txt de ghi tung dung tich nuoc cua sinhvien
		id_Voinuoc = Open("voinuoc.txt", 0);
		if (id_Voinuoc == -1)
		{
			Close(id_SV);
			Up("main"); // tro ve tien trinh chinh
			return;
		}

		// Ghi dung tich vao file voinuoc.txt tu file sinhvien.txt
		while (p_File < fileSize)
		{
			flag_VN = 0;
			Read(&temp, 1, id_SV);
			if (temp != ' ')
			{
				Write(&temp, 1, id_Voinuoc);
			}
			else
			{
				flag_VN = 1;
			}

			if (p_File == fileSize - 1)
			{
				Write("*", 1, id_Voinuoc);
				flag_VN = 1;
			}

			if (flag_VN == 1)
			{
				Close(id_Voinuoc);
				Up("voinuoc");
				// Dung chuong trinh sinhvien lai de voinuoc thuc thi
				Down("sinhvien");

				// Tao file voinuoc.txt
				if (CreateFile("voinuoc.txt") == -1)
				{
					Close(id_SV);
					Up("main"); // tro ve tien trinh chinh
					return;
				}

				// Mo file voinuoc.txt de ghi tung dung tich nuoc cua sinhvien
				id_Voinuoc = Open("voinuoc.txt", 0);
				if (id_Voinuoc == -1)
				{
					Close(id_SV);
					Up("main"); // tro ve tien trinh chinh
					return;
				}
			}
			p_File++;
		}
		Close(id_SV);
		// Ket thuc tien trinh sinhvien va voinuoc quay lai ham main
		Up("main");
	}
	// Quay lai ham main
}
