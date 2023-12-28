// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#include "syscall.h"

int a[100];

int main()
{
    int i, j, temp;

    int n;
    PrintString("Nhap vao so phan tu cua mang (toi da 100 phan tu): ");
    n = ReadInt();

    // Do neu nhap vao string ReadInt tra ve 0 nen ta xet n<=0 se bao gom ca truong hop n la string hoac so thuc vaf n <= 0
    while (n <= 0 || n > 100)
    {
        PrintString("\nn khong hop le! Moi nhap lai so phan tu cua mang (1<=n<=100): ");
        n = ReadInt();
    }

    for (i = 0; i < n; i++)
    {
        // Xuat ra cau dan
        PrintString("Moi nhap vao phan tu thu ");
        PrintInt(i + 1);
        PrintString(": ");
        // Xuat xong cau dan

        // Neu nguoi dung nhap vao khong phai so nguyen ReadInt tra ve 0 nen se khong phat hien duoc a[i]=0 that hay a[i] bi nhap sai!
        a[i] = ReadInt();
    }

    for (i = 0; i < n - 1; i++)
    {
        for (j = n - 1; j > i; j--)
        {
            if (a[j] < a[j - 1])
            {
                temp = a[j];
                a[j] = a[j - 1];
                a[j - 1] = temp;
            }
        }
    }

    for (i = 0; i < n; i++)
    {
        PrintInt(a[i]);
        PrintChar(' ');
    }
    PrintChar('\n');
    Halt();
}