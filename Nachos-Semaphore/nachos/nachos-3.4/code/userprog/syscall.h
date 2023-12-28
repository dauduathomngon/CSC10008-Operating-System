/* syscalls.h
 * 	Nachos system call interface.  These are Nachos kernel operations
 * 	that can be invoked from user programs, by trapping to the kernel
 *	via the "syscall" instruction.
 *
 *	This file is included by user programs and by the Nachos kernel.
 *
 * Copyright (c) 1992-1993 The Regents of the University of California.
 * All rights reserved.  See copyright.h for copyright notice and limitation
 * of liability and disclaimer of warranty provisions.
 */

#ifndef SYSCALLS_H
#define SYSCALLS_H

#include "copyright.h"

/* system call codes -- used by the stubs to tell the kernel which system call
 * is being asked for
 */
#define SC_Halt 0
#define SC_Exit 1
#define SC_Exec 2
#define SC_Join 3
#define SC_CreateFile 4
#define SC_Open 5
#define SC_Read 6
#define SC_Write 7
#define SC_Close 8
#define SC_Fork 9
#define SC_Yield 10

/*
 * Khai bao cac system call code
 */
#define SC_ReadInt 11
#define SC_PrintInt 12
#define SC_ReadChar 13
#define SC_PrintChar 14
#define SC_ReadString 15
#define SC_PrintString 16

// dung de di chuyen trong file
#define SC_Seek 17

// Syscall Semaphore
#define SC_CreateSemaphore 18
#define SC_Down 19
#define SC_Up 20

#ifndef IN_ASM

/* The system call interface.  These are the operations the Nachos
 * kernel needs to support, to be able to run user programs.
 *
 * Each of these is invoked by a user program by simply calling the
 * procedure; an assembly language stub stuffs the system call code
 * into a register, and traps to the kernel.  The kernel procedures
 * are then invoked in the Nachos kernel, after appropriate error checking,
 * from the system call entry point in exception.cc.
 */

/* Stop Nachos, and print out performance stats */
void Halt();

/* A unique identifier for an executing user program (address space) */
typedef int SpaceId;

/* File system operations: Create, Open, Read, Write, Close
 * These functions are patterned after UNIX -- files represent
 * both files *and* hardware I/O devices.
 *
 * If this assignment is done before doing the file system assignment,
 * note that the Nachos file system has a stub implementation, which
 * will work for the purposes of testing out these routines.
 */

/* A unique identifier for an open Nachos file. */
typedef int OpenFileId;

/* when an address space starts up, it has two open files, representing
 * keyboard input and display output (in UNIX terms, stdin and stdout).
 * Read and Write can be used directly on these, without first opening
 * the console device.
 */

#define ConsoleInput 0
#define ConsoleOutput 1

/* User-level thread operations: Fork and Yield.  To allow multiple
 * threads to run within a user program.
 */

/* Fork a thread to run a procedure ("func") in the *same* address space
 * as the current thread.
 */
void Fork(void (*func)());

/* Yield the CPU to another runnable thread, whether in this address space
 * or not.
 */
void Yield();

// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

// doc so nguyen
int ReadInt();

// in so nguyen
void PrintInt(int input);

// doc char
char ReadChar();

// in char
void PrintChar(char c);

// doc string
void ReadString(char *buffer, int length);

// in string
void PrintString(char *buffer);

/*
 * Di chuyen den vi tri chi dinh trong file
 */
int Seek(int position, OpenFileId file);

/*
 * Mo file co name va type va tra ve ID
 */
OpenFileId Open(char *name, int type);

/*
 * Dong file voi ID
 */
int Close(OpenFileId id);

/*
 * Thuc hien doc file sau do ghi vao buffer
 */
int Read(char *buffer, int charCount, OpenFileId id);

/*
 * Thuc hien ghi buffer vao file
 */
int Write(char *buffer, int charCount, OpenFileId id);

/*
 * Thuc hien tao file voi ten "name"
 */
int CreateFile(char *name);

/*
 * Thuc hien tao semaphore
 */
int CreateSemaphore(char *name, int semval);

int Down(char *name);

int Up(char *name);

/*
 * Chay file thuc thi, luu trong Nachos file ten la "name" va tra ve address space indentifier
 */
SpaceId Exec(char *name);

/*
 * Chi return 1 lan khi chuong trinh nguoi dung voi "id" da chay xong
 * Tra ve trang thai Exit
 */
int Join(SpaceId id);

/*
 * Chuong trinh nguoi dung da chay xong
 */
void Exit(int status);

#endif /* IN_ASM */

#endif /* SYSCALL_H */