// exception.cc
//	Entry point into the Nachos kernel from user programs.
//	There are two kinds of things that can cause control to
//	transfer back to here from user code:
//
//	syscall -- The user code explicitly requests to call a procedure
//	in the Nachos kernel.  Right now, the only function we support is
//	"Halt".
//
//	exceptions -- The user code does something that the CPU can't handle.
//	For instance, accessing memory that doesn't exist, arithmetic errors,
//	etc.
//
//	Interrupts (which can also cause control to transfer from user
//	code into the Nachos kernel) are handled elsewhere.
//
// For now, this only handles the Halt() system call.
// Everything else core dumps.
//
// Copyright (c) 1992-1993 The Regents of the University of California.
// All rights reserved.  See copyright.h for copyright notice and limitation
// of liability and disclaimer of warranty provisions.

#include "copyright.h"
#include "system.h"
#include "syscall.h"

//----------------------------------------------------------------------
// ExceptionHandler
// 	Entry point into the Nachos kernel.  Called when a user program
//	is executing, and either does a syscall, or generates an addressing
//	or arithmetic exception.
//
// 	For system calls, the following is the calling convention:
//
// 	system call code -- r2
//		arg1 -- r4
//		arg2 -- r5
//		arg3 -- r6
//		arg4 -- r7
//
//	The result of the system call, if any, must be put back into r2.
//
// And don't forget to increment the pc before returning. (Or else you'll
// loop making the same system call forever!
//
//	"which" is the kind of exception.  The list of possible exceptions
//	are in machine.h.

#define MAX_FILE_NAME 32
#define MAX_CHAR 255

// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

// Input:
//	- Dia chi cua user space (int)
//	- Do dai toi da cua buffer (int), thong thuong la 255
// Output: Buffer (char*)
// Purpose: Copy buffer tu system space chuyen sang cho user space
char *User2System(int virtAddr, int limit)
{
    int i; // chi so index
    int oneChar;
    char *kernelBuf = NULL;
    kernelBuf = new char[limit + 1]; // can cho chuoi terminal
    if (kernelBuf == NULL)
        return kernelBuf;

    memset(kernelBuf, 0, limit + 1);

    for (i = 0; i < limit; i++)
    {
        machine->ReadMem(virtAddr + i, 1, &oneChar);
        kernelBuf[i] = (char)oneChar;
        if (oneChar == 0)
            break;
    }
    return kernelBuf;
}

// Input:
// 	- Dia chi cua user space (int)
//	- Do dai toi da cua buffer (int)
//	- Buffer (char*)
// Output: So luong bytes copy tu system sang user
// Purpose: Copy buffer tu System space sang User space
int System2User(int virtAddr, int len, char *buffer)
{
    if (len < 0)
        return -1;
    if (len == 0)
        return len;
    int i = 0;
    int oneChar = 0;
    do
    {
        oneChar = (int)buffer[i];
        machine->WriteMem(virtAddr + i, 1, oneChar);
        i++;
    } while (i < len && oneChar != 0);
    return i;
}

//----------------------------------------------------------------------
// 	Cac quy dinh su dung thanh ghi:
// 	   1. Thanh ghi 2: Chua ma lenh syscall va ket qua thuc hien o syscall se
//        tra nguoc ve
// 	   2. Thanh ghi 4: Tham so thu nhat
//	   3. Thanh ghi 5: Tham so thu hai
//	   4. Thanh ghi 6: Tham so thu ba
//	   5. Thanh ghi 7: Tham so thu tu
//----------------------------------------------------------------------

// Tang thanh ghi
void IncreasePC()
{
    int pcAfter = machine->registers[NextPCReg] + 4;           // tang next PC len 4 (vi int 4 byte)
    machine->registers[PrevPCReg] = machine->registers[PCReg]; // gan previous PC register = current PC register
    machine->registers[PCReg] = machine->registers[NextPCReg]; // gan current PC register = next PC register
    machine->registers[NextPCReg] = pcAfter;
}

void ExceptionHandler(ExceptionType which)
{
    int type = machine->ReadRegister(2);

    switch (which)
    {
    case NoException:
        return;

    case PageFaultException:
    {
        DEBUG('a', "\nPage fault.");
        printf("\nPage fault.\n");
        interrupt->Halt();
        break;
    }

    case ReadOnlyException:
    {
        DEBUG('a', "\nPage marked read-only");
        printf("\nPage marked read-only\n");
        interrupt->Halt();
        break;
    }

    case BusErrorException:
    {
        DEBUG('a', "\nInvalid physical address");
        printf("\nInvalid physical address.\n");
        interrupt->Halt();
        break;
    }

    case AddressErrorException:
    {
        DEBUG('a', "\n Address error.");
        printf("\n Address error.\n");
        interrupt->Halt();
        break;
    }

    case OverflowException:
    {
        DEBUG('a', "\nOverflow !!!");
        printf("\nOverflow !!!\n");
        interrupt->Halt();
        break;
    }

    case IllegalInstrException:
    {
        DEBUG('a', "\nIllegal instruction.");
        printf("\nIllegal instruction.\n");
        interrupt->Halt();
        break;
    }

    case NumExceptionTypes:
    {
        DEBUG('a', "\nNumber exception types");
        printf("\nNumber exception types\n");
        interrupt->Halt();
        break;
    }

    case SyscallException:
    {
        switch (type)
        {
        case SC_Halt:
        {
            /* Summary: Ham dung de tat chuong trinh
             * Input: Khong co
             * Output: Thong bao tat chuong trinh
             */
            DEBUG('a', "Shutdown, initiated by user program.\n");
            interrupt->Halt();
            return;
        }

        case SC_PrintString:
        {
            /* Summary: Ham dung de in ra string
             * Input: char* buffer (string duoc nhap vao)
             * Output: In ra string duoc nhap vao
             */
            int virtualAddress;
            char *buf;

            // Lấy địa chỉ từ thanh ghi thứ 4
            virtualAddress = machine->ReadRegister(4);

            // Biến buf của kernel lấy từ user (địa chỉ chuỗi từ thanh
            // ghi thứ 4)
            buf = User2System(virtualAddress, 255);

            int size = 0;
            while (buf[size] != '\0')
                size++;

            synchcons->Write(buf, size + 1);

            delete buf;

            IncreasePC();
            return;
        }

        case SC_ReadChar:
        {
            /* Summary: Ham dung de doc mot ky tu (char)
             * Input: Khong co
             * Output: Tra ve ky tu doc duoc (neu khong phai ky tu hop le, tra ve ky tu rong)
             */
            char *buffer = new char[255]();
            int length = synchcons->Read(buffer, 255);

            if (length > 1)
            {
                DEBUG('a', "\nERROR: Chi duoc nhap duy nhat 1 ky tu!");
                machine->WriteRegister(2, 0);
            }
            else if (length == 0)
            {
                DEBUG('a', "\nERROR: Ky tu rong!");
                machine->WriteRegister(2, 0);
            }
            else
            {
                char result = buffer[0];
                machine->WriteRegister(2, result);
            }

            delete buffer;
            IncreasePC();
            return;
        }

        case SC_PrintChar:
        {
            /* Summary: Ham dung de in ra ky tu (char)
             * Input: char* c (ky tu duoc nhap vao)
             * Output: In ra ky tu duoc nhap vao
             */
            char c = machine->ReadRegister(4);

            synchcons->Write(&c, 1);

            IncreasePC();
            return;
        }

        case SC_PrintInt:
        {
            /* Summary: Ham dung de in ra so nguyen (int)
             * Input: int input (so nguyen duoc nhap vao)
             * Output: In ra so nguyen duoc nhap vao
             */
            int number = machine->ReadRegister(4);
            if (number < 10 && number >= 0)
            {
                char output = number + '0';
                synchcons->Write(&output, 1);
                IncreasePC();
                return;
            }

            bool is_negative = false;
            if (number < 0)
            {
                is_negative = true;
                number *= -1;
            }

            char *buffer = new char[255 + 1]();
            int idx = 0;
            while (number > 0)
            {
                buffer[idx++] = (number % 10) + '0';
                number /= 10;
            }

            if (is_negative)
                buffer[idx] = '-';

            // reverse buffer
            int i;
            char *reverse = new char[255 + 1]();
            for (i = idx; i >= 0; i--)
            {
                reverse[idx - i] = buffer[i];
            }
            reverse[++idx] = '\0';

            synchcons->Write(reverse, idx + 1);

            delete buffer;
            delete reverse;

            IncreasePC();
            break;
        }

        case SC_ReadString:
        {
            /* Summary: Ham dung de doc mot string
             * Input: Khong co
             * Output: Tra ve string doc duoc
             */
            int virtualAddress = machine->ReadRegister(4);
            int length = machine->ReadRegister(5);

            char *buffer;
            buffer = User2System(virtualAddress, length);

            synchcons->Read(buffer, length);
            System2User(virtualAddress, length, buffer);

            delete buffer;
            IncreasePC();
            break;
        }

        case SC_ReadInt:
        {
            /* Summary: Ham dung de doc mot so nguyen (int)
             * Input: Khong co
             * Output: Tra ve so nguyen doc duoc (neu khong phai so nguyen hop le, tra ve 0)
             * Note: Ngoai ra so -354.0000000 cung duoc tinh la so nguyen -354
             */
            char *buffer = new char[255]();
            int maxBuffer = 255;
            int sign = 1;
            int start = 0;
            int i, j;
            int result = 0;
            int after_dot = 0;
            int size = synchcons->Read(buffer, maxBuffer);

            if (buffer[0] == '-')
            {
                // Bat dau doc tu 1
                sign = -1;
                start = 1;
            }

            // check invalid number
            for (i = start; i < size; i++)
            {
                if (buffer[i] < '0' || buffer[i] > '9')
                {
                    if (buffer[i] == '.') // for example: 18.0000 is also a integer
                    {
                        after_dot++;
                        for (j = i + 1; j < size; j++)
                        {
                            if (buffer[j] != '0')
                            {
                                DEBUG('a', "\nERROR: input khong phai la so!");
                                machine->WriteRegister(2, 0);
                                IncreasePC();
                                return;
                            }
                            after_dot++;
                        }
                        break;
                    }
                    else
                    {
                        DEBUG('a', "\nERROR: input khong phai la so!");
                        machine->WriteRegister(2, 0);
                        IncreasePC();
                        return;
                    }
                }
            }

            // prevent overflow
            char *max_int = "2147483647";
            int max_length = 10;
            int real_size = size - after_dot;

            if (((start == 1) && (real_size == max_length + 1)) || ((start == 0) && (real_size == max_length)))
            {
                for (i = 0; i < max_length; i++)
                {
                    if (buffer[i + start] - '0' > max_int[i] - '0')
                    {
                        DEBUG('a', "\nERROR: Overflow!");
                        machine->WriteRegister(2, 0);
                        delete buffer;
                        IncreasePC();
                        return;
                    }
                }
            }
            else if (((start == 1) && (real_size > max_length + 1)) || ((start == 0) && (real_size > max_length)))
            {
                DEBUG('a', "\nERROR: Overflow!");
                machine->WriteRegister(2, 0);
                delete buffer;
                IncreasePC();
                return;
            }

            // turn buffer to number
            for (i = start; i < real_size; i++)
            {
                result = result * 10 + (buffer[i] - '0');
            }
            result *= sign;

            machine->WriteRegister(2, result);

            delete buffer;
            IncreasePC();
            break;
        }

        // syscall file
        case SC_CreateFile:
        {
            /*
             * Summary: Tao 1 file, file nam tai thu muc code
             * Input: Ten cua file (char*)
             * Output: -1 (khong thanh cong), 0 (thanh cong)
             */
            int bufAddr;
            bufAddr = machine->ReadRegister(4); // doc dia chi input

            char *buf;
            buf = User2System(bufAddr, MAX_CHAR + 1);

            if (buf == NULL)
            {
                printf("\nERROR: Khong the doc ten file");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            if (fileSystem->Create(buf, 0) == false)
            {
                printf("\nERROR: Khong the tao file");
                machine->WriteRegister(2, -1);
                delete[] buf;
                IncreasePC();
                break;
            }

            machine->WriteRegister(2, 0);
            delete[] buf;
            IncreasePC();
            return;
        }
        case SC_Seek:
        {
            /*
             * Summary: Di den vi tri (position) trong file
             * Input: vi tri can den (int) va ID cua file (int)
             * Output: -1 (khong thanh cong), vi tri da di den (thanh cong)
             */

            int pos = machine->ReadRegister(4); // Lay vi tri can chuyen con tro den trong file
            int id = machine->ReadRegister(5);  // Lay id cua file
            // Kiem tra id cua file truyen vao co nam ngoai bang mo ta file khong
            if (id < 0 || id > 14)
            {
                printf("\nKhong the seek vi id nam ngoai bang mo ta file.");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }
            // Kiem tra file co ton tai khong
            if (fileSystem->openf[id] == NULL)
            {
                printf("\nKhong the seek vi file nay khong ton tai.");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }
            // Kiem tra co goi Seek tren console khong
            if (id == 0 || id == 1)
            {
                printf("\nKhong the seek tren file console.");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }
            // Neu pos = -1 thi gan pos = Length nguoc lai thi giu nguyen pos
            pos = (pos == -1) ? fileSystem->openf[id]->Length() : pos;
            if (pos > fileSystem->openf[id]->Length() || pos < 0) // Kiem tra lai vi tri pos co hop le khong
            {
                printf("\nKhong the seek file den vi tri nay.");
                machine->WriteRegister(2, -1);
            }
            else
            {
                // Neu hop le thi tra ve vi tri di chuyen thuc su trong file
                fileSystem->openf[id]->Seek(pos);
                machine->WriteRegister(2, pos);
            }
            IncreasePC();
            return;
        }
        case SC_Open:
        {
            /*
             * Summary: Mo file de dung cho viec doc hoac ghi
             * Input: ten file (char*) va loai cua file (int)
             * Output: ID cua file trong bang mo ta file neu thanh cong, -1 neu khong thanh cong
             */
            int virtAddr;
            int type;
            char *filename;

            // check for exception
            virtAddr = machine->ReadRegister(4); // Doc dia chi cua ten file tai thanh ghi R4
            type = machine->ReadRegister(5);     // doc type tai thanh ghi R5

            filename = User2System(virtAddr, MAX_FILE_NAME);

            // Neu ten file khong co
            if (strlen(filename) == 0)
            {
                printf("\nERROR: Ten file khong ton tai");
                machine->WriteRegister(2, -1);
                delete filename;
                IncreasePC();
                return;
            }

            int NullPos = fileSystem->FindFreeSlot();

            if (NullPos != -1) // Neu con vi tri trong
            {
                // stdin
                if (type == 2)
                {
                    machine->WriteRegister(2, 0);
                }

                // stdout
                else if (type == 3)
                {
                    machine->WriteRegister(2, 1);
                }

                else if (type == 0 || type == 1)
                {
                    fileSystem->openf[NullPos] = fileSystem->Open(filename, type);

                    // Neu khong tim thay file trong directory
                    if (fileSystem->openf[NullPos] == NULL)
                    {
                        printf("\nERROR: Khong tim thay file");
                        machine->WriteRegister(2, -1);
                    }

                    // Mo file thanh cong
                    if (fileSystem->openf[NullPos] != NULL)
                    {
                        machine->WriteRegister(2, NullPos);
                    }
                }
                delete filename;
                IncreasePC();
                return;
            }
            machine->WriteRegister(2, -1);
            delete filename;

            IncreasePC();
            return;
        }
        case SC_Close:
        {
            /*
             * Summary: Dong file voi ID
             * Input: ID cua file can dong
             */
            int fileID;

            // Lay tham so ID tu thanh ghi R4
            fileID = machine->ReadRegister(4);

            // Nam trong bang mo ta [0, 9]
            if (fileID <= 9 && fileID >= 0)
            {
                // Ton tai file
                if (fileSystem->openf[fileID] != NULL)
                {
                    delete fileSystem->openf[fileID];
                    fileSystem->openf[fileID] = NULL;
                    machine->WriteRegister(2, 0);
                    IncreasePC();
                    return;
                }
            }
            printf("\nERROR: Khong the dong file");
            machine->WriteRegister(2, -1);
            IncreasePC();
            return;
        }
        case SC_Read:
        {
            /*
             * Summary: Doc file va ghi vao buffer
             * Input: buffer (char*), so ky tu (int), id cua file (int)
             * Output: -1 (khong doc duoc), so bytes doc (thanh cong)
             */
            // Lay dia chi ten file
            int virtAddr = machine->ReadRegister(4);

            // Lay so ki tu cho phep
            int charcount = machine->ReadRegister(5);

            // Lay id file
            int id = machine->ReadRegister(6);

            // Neu id file khong nam trong bang mo ta file
            if (id > 9 || id < 0)
            {
                printf("\nERROR: Khong nam trong bang mo ta file");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            // Neu file khong ton tai
            if (fileSystem->openf[id] == NULL)
            {
                printf("\nERROR: File khong ton tai");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            // Neu file la stdout (type == 3)
            if (fileSystem->openf[id]->type == 3)
            {
                printf("\nERROR: Khong the doc stdout");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            // Bo dem de xu li giua User Space va System Space
            char *tempBuffer = User2System(virtAddr, charcount);

            // Lay vi tri dau tien cua file noi con tro dang tro toi
            int beginPos = fileSystem->openf[id]->GetCurrentPos();

            // Neu file la stdin (type == 2)
            if (fileSystem->openf[id]->type == 2)
            {
                // Read file va tra ve so byte thuc su doc duoc
                int numBytes = synchcons->Read(tempBuffer, charcount);

                System2User(virtAddr, numBytes, tempBuffer);

                // Tra ve so byte thuc su doc duoc
                machine->WriteRegister(2, numBytes);
                delete tempBuffer;
                IncreasePC();
                return;
            }

            // File binh thuong
            int checker = fileSystem->openf[id]->Read(tempBuffer, charcount);

            // Doc file thanh cong
            if (checker > 0)
            {
                int endPos = fileSystem->openf[id]->GetCurrentPos();
                int numBytes = endPos - beginPos;

                System2User(virtAddr, numBytes, tempBuffer);
                machine->WriteRegister(2, numBytes);
            }
            // Cuoi file -> file rong -> doc NULL
            else
            {
                machine->WriteRegister(2, -2);
            }

            delete tempBuffer;
            IncreasePC();
            return;
        }
        case SC_Write:
        {
            /*
             * Summary: Ham de ghi buffer vao file
             * Input: buffer (char*), so ky tu (int), id cua file (int)
             * Output: -1 (khong ghi duoc), so bytes ghi (thanh cong)
             */
            int virtualAddress = machine->ReadRegister(4); // lay dia chi cua buffer
            int charCount = machine->ReadRegister(5);      // lay so ky tu
            int fileID = machine->ReadRegister(6);         // lay id cua file

            int currentPos; // vi tri hien tai cua file
            int newPos;     // vi tri moi sau khi write
            char *buf;      // chuoi ky tu doc duoc

            // id cua file phai nam trong bang mo ta file (co gia tri tu 0->14).
            if (fileID < 0 || fileID > 9)
            {
                printf("\nERROR: File nam ngoai bang mo ta file");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            // file khong ton tai
            if (fileSystem->openf[fileID] == NULL)
            {
                printf("\nERROR: File khong ton tai");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            // file input (stdin, type la 2)
            if (fileSystem->openf[fileID]->type == 2)
            {
                printf("\nERROR: File stdin khong the write duoc");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            // file chi doc (only read, type la 1)
            if (fileSystem->openf[fileID]->type == 1)
            {
                printf("\nERROR: File chi doc");
                machine->WriteRegister(2, -1);
                IncreasePC();
                return;
            }

            currentPos = fileSystem->openf[fileID]->GetCurrentPos();
            // copy chuoi tu user space sang system space
            buf = User2System(virtualAddress, charCount);

            // truong hop 1: ghi thang vao file, khi do tra ve so bytes thuc su da ghi
            // nhung file ghi duoc se co type = 0 (read and write file)
            if (fileSystem->openf[fileID]->type == 0)
            {
                // ghi thanh cong
                if (fileSystem->openf[fileID]->Write(buf, charCount) > 0)
                {
                    newPos = fileSystem->openf[fileID]->GetCurrentPos();
                    machine->WriteRegister(2, newPos - currentPos);
                    delete buf;
                    IncreasePC();
                    return;
                }
            }

            // truong hop 2: ghi vao file stdout (xuat len console)
            if (fileSystem->openf[fileID]->type == 3)
            {
                int size = 0;
                while (buf[size] != '\0')
                    size++;
                // ghi len console
                synchcons->Write(buf, size + 1);
                // tra ve so byte thuc su ghi
                machine->WriteRegister(2, size);
                delete buf;
                IncreasePC();
                return;
            }
        }

        // syscall dong bo hoa
        case SC_CreateSemaphore:
        {
            int virtAddr = machine->ReadRegister(4);
            int semval = machine->ReadRegister(5);

            char *name = User2System(virtAddr, MAX_CHAR + 1);
            if (name == NULL)
            {
                printf("\nERROR: Khong du bo nho trong System");
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                break;
            }

            int res = sTab->Create(name, semval);

            if (res == -1)
            {
                printf("\nERROR: Khong the khoi tao Semaphore");
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                break;
            }

            delete[] name;
            machine->WriteRegister(2, res);
            IncreasePC();
            break;
        }
        case SC_Down:
        {
            int virtualAddress;
            virtualAddress = machine->ReadRegister(4);
            char *name;
            name = User2System(virtualAddress, MAX_CHAR + 1);

            if (name == NULL)
            {
                printf("\nERROR: Khong du bo nho trong System");
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                break;
            }

            int res = sTab->Wait(name);

            if (res == -1)
            {
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                break;
            }

            delete[] name;
            machine->WriteRegister(2, res);
            IncreasePC();
            return;
        }
        case SC_Up:
        {
            int virtualAddress;
            virtualAddress = machine->ReadRegister(4);
            char *name;
            name = User2System(virtualAddress, MAX_CHAR + 1);

            if (name == NULL)
            {
                printf("\nERROR: Khong du bo nho trong System");
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                break;
            }

            int res = sTab->Signal(name);

            if (res == -1)
            {
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                break;
            }

            delete[] name;
            machine->WriteRegister(2, res);
            IncreasePC();
            return;
        }
        case SC_Exec:
        {
            /*
             * Summary: Chay 1 file voi ten "name" duoc truyen vao
             * Input: Ten file (char*)
             * Output: -1 (that bai), id cua process neu thanh cong
             */

            int virtualAddress;
            virtualAddress = machine->ReadRegister(4); // doc dia chi chua ten cua chuong trinh
            char *name;
            name = User2System(virtualAddress, MAX_CHAR + 1); // lay ten cua chuong trinh

            if (name == NULL)
            {
                printf("\nERROR: Ten khong hop le");
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                return;
            }

            // thu xem file mo duoc khong
            OpenFile *file = fileSystem->Open(name);
            if (file == NULL)
            {
                machine->WriteRegister(2, -1);
                delete[] name;
                IncreasePC();
                return;
            }
            delete file;

            // cho chay tien trinh
            int id = pTab->ExecUpdate(name);
            machine->WriteRegister(2, id);
            delete[] name;
            IncreasePC();
            return;
        }
        case SC_Join:
        {
            int id;
            id = machine->ReadRegister(4);
            int res;
            res = pTab->JoinUpdate(id);
            machine->WriteRegister(2, res);
            IncreasePC();
            return;
        }
		case SC_Exit:
		{
			int exitStatus = machine->ReadRegister(4);
			if (exitStatus != 0)
			{
				IncreasePC();
				return;
			}
			pTab->ExitUpdate(exitStatus);
			currentThread->FreeSpace();
			currentThread->Finish();
			IncreasePC();
			return;
		}
        }
    }
    }
}
