// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#include "syscall.h"

#define MAX_FILE_NAME 32
#define MAX_CHAR 255

int main()
{
	int openFileID; // id cua file
	int fileSize; // size cua file
	char fileName[MAX_FILE_NAME]; // ten cua file
	int i;
	char c; // ky tu de in ra man hinh
	char writeBuffer[MAX_CHAR];
	int writeSize;
	
	PrintString("Moi ban nhap ten file: ");
	ReadString(fileName, MAX_FILE_NAME);
	
	PrintString("Ten file da chon: ");
	PrintString(fileName);
	PrintString("\n");
	
	openFileID = Open(fileName, 0);
	
	// file khong bi loi
	if (openFileID == -1)
	{
		PrintString("ERROR: Mo file khong thanh cong \n");
		Halt();
	}
	
	PrintString("Thanh cong mo file ");
	PrintString(fileName);
	PrintString(" voi ID: ");
	PrintInt(openFileID);
	PrintString("\n\n");
	
	PrintString("-----------------------------------------------\n");
	PrintString("Tien hanh doc file: ");
	PrintString(fileName);
	PrintString("\n");
	
	// dau tien di den cuoi file de lay do dai file
	fileSize = Seek(-1, openFileID);
	if (fileSize == -1)
	{
		PrintString("ERROR: Khong the di chuyen trong file \n");
		Halt();
	}
	
	PrintString("Do dai cua file la: ");
	PrintInt(fileSize);
	PrintString("\n");
	
	// sau do quay ve dau file de doc
	Seek(0, openFileID);
	
	PrintString("Nhung gi doc duoc: \n");
	
	// tien hanh doc file
	for (i = 0; i < fileSize; i++)
	{
		Read(&c, 1, openFileID);
		PrintChar(c);
	}
	PrintString("\n-----------------------------------------------\n\n");
	
	// ghi file
	PrintString("-----------------------------------------------\n");
	PrintString("Tien hanh doc file: ");
	PrintString(fileName);
	PrintString("\n");
	
	// dau tien doc buffer can ghi
	PrintString("Nhap noi dung muon ghi (toi da 255 ki tu): ");
	ReadString(writeBuffer, MAX_CHAR);
	
	while (writeBuffer[writeSize] != '\0')
		writeSize++;
	for (i = 0; i < writeSize; i++)
	{
		Write(&writeBuffer[i], 1, openFileID);
	}
	
	PrintString("----------------------------------------------\n\n");
	
	// tien hanh doc file lan nua de thay khac biet
	PrintString("-----------------------------------------------\n");
	PrintString("Tien hanh doc file: ");
	PrintString(fileName);
	PrintString("\n");
	
	// dau tien di den cuoi file de lay do dai file
	fileSize = Seek(-1, openFileID);
	if (fileSize == -1)
	{
		PrintString("ERROR: Khong the di chuyen trong file \n");
		Halt();
	}
	
	PrintString("Do dai cua file la: ");
	PrintInt(fileSize);
	PrintString("\n");
	
	// sau do quay ve dau file de doc
	Seek(0, openFileID);
	
	PrintString("Nhung gi doc duoc: \n");
	
	// tien hanh doc file
	for (i = 0; i < fileSize; i++)
	{
		Read(&c, 1, openFileID);
		PrintChar(c);
	}
	PrintString("\n-----------------------------------------------\n\n");
	
	Close(openFileID);
	Halt();
}