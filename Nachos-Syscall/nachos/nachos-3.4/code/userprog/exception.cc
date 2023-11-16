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

// Input:
//	- Dia chi cua user space (int)
//	- Do dai toi da cua buffer (int), thong thuong la 255
// Output: Buffer (char*)
// Purpose: Copy buffer tu system space chuyen sang cho user space
char* User2System(int virtAddr,int limit)
{
	int i;// index
	int oneChar;
	char* kernelBuf = NULL;

	kernelBuf = new char[limit +1];//need for terminal string
				       //
	if (kernelBuf == NULL)
		return kernelBuf;

	memset(kernelBuf,0,limit+1);

	for (i = 0 ; i < limit ;i++)
	{
		machine->ReadMem(virtAddr+i,1,&oneChar);
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
int System2User(int virtAddr, int len, char* buffer)
{
	if (len < 0)
		return -1;

	if (len == 0)
		return len;

	int i = 0;
	int oneChar = 0 ;
	do
	{
		oneChar= (int) buffer[i];
		machine->WriteMem(virtAddr+i,1,oneChar);
		i ++;
	} while(i < len && oneChar != 0);

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
void IncreasePC(){
    // Plus 4 for moving to next command
    int nextPC= machine->registers[NextPCReg]+4;
    machine->registers[PrevPCReg]=machine->registers[PCReg];
    machine->registers[PCReg]=machine->registers[NextPCReg];
    machine->registers[NextPCReg]= nextPC;
}

void
ExceptionHandler(ExceptionType which)
{
    int type = machine->ReadRegister(2);

    switch (which)
	{
	case NoException:
	    return;

	case PageFaultException:
	{
	    DEBUG('a', "\nPage fault.");
	    printf("\n\nPage fault.");
	    interrupt->Halt();
	    break;
	}

	case ReadOnlyException:
	{
		DEBUG('a', "\nPage marked read-only");
		printf("\n\nPage marked read-only");
		interrupt->Halt();
		break;
	}

	case BusErrorException:
	{
        DEBUG('a', "\nInvalid physical address");
		printf("\n\nInvalid physical address");
		interrupt->Halt();
		break;
	}

	case AddressErrorException:
	{
		DEBUG('a', "\n Address error.");
		printf("\n\n Address error.");
		interrupt->Halt();
		break;
	}

	case OverflowException:
	{
		DEBUG('a', "\nOverflow !!!");
		printf("\n\nOverflow !!!");
		interrupt->Halt();
		break;
	}

	case IllegalInstrException:
	{
		DEBUG('a', "\nIllegal instr.");
		printf("\n\nIllegal instr.");
		interrupt->Halt();
		break;
	}

	case NumExceptionTypes:
	{
		DEBUG('a', "\nNumber exception types");
		printf("\n\nNumber exception types");
		interrupt->Halt();
		break;
	}

	case SyscallException:
	{
		switch (type)
		{
		case SC_Halt:
		{
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
			int virtualAddress;
			char* buf;

			// Lấy địa chỉ từ thanh ghi thứ 4
			virtualAddress = machine->ReadRegister(4);

			// Biến buf của kernel lấy từ user (địa chỉ chuỗi từ thanh
			// ghi thứ 4)
			buf = User2System(virtualAddress, 255);

			int size = 0;
			while (buf[size] != '\0') size++;

			synchcons->Write(buf, size + 1);

			delete buf;

			IncreasePC();
			break;
		}

		case SC_PrintChar:
		{
			char c = (char)machine->ReadRegister(4);

			synchcons->Write(&c,1);

			IncreasePC();
			break;
		}

		// => Cac anh se viet tiep o day
		case SC_PrintInt:
		{
			int number = machine->ReadRegister(4);
			if (number < 10 && number > 0)
			{
				char output = number + '0';
				synchcons->Write(&output, 1);
				IncreasePC();
				break;
			}

			bool is_negative = false;
			if (number < 0)
			{
				is_negative = true;
				number *= -1;
			}

			char* buffer = new char[255 + 1]();
			int idx = 0;
			while (number > 0)
			{
				buffer[idx++] = (number % 10) + '0';
				number /= 10;
			}

			if (is_negative)
				buffer[idx] = '-';

			// reverse buffer
			int i = idx;
			char* reverse = new char[255 + 1]();
			for (i; i >= 0; i--)
			{
				reverse[idx - i] = buffer[i];
			}
			reverse[++idx] = '\0';

			synchcons->Write(reverse, idx+1);

			delete buffer;
			delete reverse;

			IncreasePC();
			break;
		}
		}
	}
    }
}
