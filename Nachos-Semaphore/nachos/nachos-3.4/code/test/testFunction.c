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
    char c;
    char a[255];
    int n;
	int result;
    
    PrintString("Moi ban nhap ky tu: ");
    c = ReadChar(); // done
    PrintString("Ky tu sau khi nhap: ");
    PrintChar(c);
    
    PrintString("\nMoi ban nhap so nguyen: ");
    n = ReadInt();
    PrintString("So sau khi nhap: ");
    PrintInt(n);
    
    PrintString("\nMoi ban nhap chuoi: ");
    ReadString(a, 255);
    PrintString("Chuoi sau khi nhap: ");
    PrintString(a);
	
	PrintString("\nTao semaphore name = lenguyen, semval = 1");
	result = CreateSemaphore("lenguyen", 1);
	
	if (result == 0)
	{
		PrintString("\nDa tao thanh cong semaphore");
	}
    
    PrintChar('\n');
    Halt();
}