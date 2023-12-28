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
	int i;
	for (i = 0; i < 1000; i++)
	{
		Down("ping");
		PrintChar('A');
		Up("pong");
	}

	Halt();
}