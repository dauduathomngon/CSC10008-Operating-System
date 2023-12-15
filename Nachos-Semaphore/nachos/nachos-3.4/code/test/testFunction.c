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
    
    PrintChar('\n');
    Halt();
}