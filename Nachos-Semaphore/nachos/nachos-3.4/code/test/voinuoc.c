#include "syscall.h"
#include "copyright.h"

void main()
{
	// Khai bao
	SpaceId id_Voinuoc, id_Res; // Bien id cho file
	char temp;					// Bien ki tu luu ki tu doc tu file
	int voi1, voi2;				// Voi 1, voi 2
	int dungTich;				// Dung tich nuoc cua sinh vien
	int flagDoneResult;			// Bien co luu dau hieu doc xong file result
	int len;
	char str[255];

	//-----------------------------------------------------------

	voi1 = voi2 = 0;
	// Xu ly voi nuoc
	while (1)
	{
		Down("end");

		// Mo file result.txt de ghi voi nao su dung
		id_Res = Open("result.txt", 0);
		if (id_Res == -1)
		{ //?
			Up("sinhvien");
			return;
		}

		while (1)
		{
			Down("voinuoc");
			temp = 0;
			// Mo file voi nuoc .txt de doc dung tich
			id_Voinuoc = Open("voinuoc.txt", 1);

			if (id_Voinuoc == -1)
			{
				//?
				Close(id_Res);
				Up("sinhvien");

				return;
			}

			dungTich = 0;
			len = 0;
			flagDoneResult = 0;

			while (1)
			{
				if (Read(&temp, 1, id_Voinuoc) == -2)
				{
					Close(id_Voinuoc);
					break;
				}

				if (temp != '*')
				{
					dungTich = dungTich * 10 + (temp - 48);
					str[len] = temp;
					len++;
				}
				else
				{
					flagDoneResult = 1;
					Close(id_Voinuoc);
					break;
				}
			}

			str[len] = 0;

			if (dungTich != 0)
			{
				Write(str, len, id_Res);
				Write(" ", 1, id_Res);

				// Dung voi 1
				if (voi1 <= voi2)
				{
					voi1 += dungTich;
					Write("1", 1, id_Res);
				}
				else // Dung voi 2
				{
					voi2 += dungTich;
					Write("2", 1, id_Res);
				}
				Write("  ", 2, id_Res);
			}

			if (flagDoneResult == 1)
			{
				voi1 = voi2 = 0;
				Close(id_Res);
				Up("sinhvien");
				break;
			}

			Up("sinhvien");
		}
	}
}
