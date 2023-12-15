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
    // in ra thong tin thanh vien
    PrintString("   - - - - - - - - - - - - - - \n");
    PrintString(" / Cac thanh vien trong nhom:  \\ \n| 21120508 - Dang An Nguyen     | \n| 21120312 - Phan Nguyen Phuong |\n| 21120498 - Do Hoang Long      | \n| 21120355 - Nguyen Anh Tu      | \n \\ 21120511 - Le Nguyen        / \n");
    PrintString("   - - - - - - - - - - - - - - \n");
    PrintString("     \\  ^__^\n");
    PrintString("      \\ (oo)\\_____\n");
    PrintString("        (__)\\     )\\/\\\n");
    PrintString("           ||----w |\n");
    PrintString("           ||     ||\n\n");

    // in ra huong dan su dung
    PrintString("Cac chuong trinh hien co: \n");
    PrintString("  + ascii: In ra bang ma ASCII \n");
    PrintString("  + sort: Sap xep lai mang n so nguyen (n <= 100)\n");
    PrintString("  + testFunction: test cac chuc nang ReadInt, PrintInt, ...\n");
    PrintString("Lam sao de chay chuong trinh, ta co 2 cach: \n");
    PrintString("  + Cach 1: Vao thu muc code, chay 'bash run.sh <ten chuong trinh>' \n");
    PrintString("  + Cach 2: Vao thu muc code, chay 'make' va sau do chay './userprog/nachos -rs 1023 -x ./test/<ten chuong trinh>'\n");

    Halt();
}
