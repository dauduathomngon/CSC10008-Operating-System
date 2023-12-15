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
    int i; // index
    int oneChar;
    char *kernelBuf = NULL;

    kernelBuf = new char[limit + 1]; // need for terminal string
                                     //
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
    //     // Plus 4 for moving to next command
    //     int nextPC= machine->registers[NextPCReg]+4;
    //     machine->registers[PrevPCReg]=machine->registers[PCReg];
    //     machine->registers[PCReg]=machine->registers[NextPCReg];
    //     machine->registers[NextPCReg]= nextPC;
    int counter = machine->ReadRegister(PCReg);
    machine->WriteRegister(PrevPCReg, counter);
    counter = machine->ReadRegister(NextPCReg);
    machine->WriteRegister(PCReg, counter);
    machine->WriteRegister(NextPCReg, counter + 4);
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
            break;
        }

        case SC_Exit:
        {
            Exit(0);
            break;
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
            break;
        }

        case SC_ReadChar:
        {
            /* Summary: Ham dung de doc mot ky tu (char)
             * Input: Khong co
             * Output: Tra ve ky tu doc duoc (neu khong phai ky tu hop le, tra ve ky tu rong)
             */
            char *buffer = new char[255 + 1]();
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
            break;
        }

        case SC_PrintChar:
        {
            /* Summary: Ham dung de in ra ky tu (char)
             * Input: char* c (ky tu duoc nhap vao)
             * Output: In ra ky tu duoc nhap vao
             */
            char c = (char)machine->ReadRegister(4);

            synchcons->Write(&c, 1);

            IncreasePC();
            break;
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

            char *buffer = new char[length + 1]();
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
            char *buffer = new char[255 + 1]();
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
        }
    }
    }
}