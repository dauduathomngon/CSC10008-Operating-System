// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#include "syscall.h"

int main()
{
	int min = 33;
	int max = 126;

	int i = min; // row

	PrintString("Dec:    ASCII:     Dec:     ASCII:     Dec:     ASCII:     Dec:     ASCII: \n");

	for (i; i <= max; i += 4)
	{
		int j = i;							 // column
		for (j; j <= i + 3 && j <= max; j++) // print first three value
		{
			if (j != i)
				PrintString("          ");
			PrintInt(j);
			if (j >= 100)
				PrintString("      ");
			else
				PrintString("       ");
			PrintChar((char)j);
		}
		PrintChar('\n');
	}

	PrintChar('\n');

	Halt();
}