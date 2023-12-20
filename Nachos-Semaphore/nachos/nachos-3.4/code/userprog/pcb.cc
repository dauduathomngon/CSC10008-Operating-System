// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#include "pcb.h"
#include "utility.h"
#include "system.h"
#include "thread.h"
#include "addrspace.h"

extern void StartProcessNoExec(int pid);

PCB::PCB(int id)
{
	// process dau tien (process main)
	if (id == 0)
		this->parentID = -1;
	else
		this->parentID = currentThread->processID;

	// tien trinh van chua duoc chay
	this->m_thread = NULL;

	this->numWait = 0;
	this->exitcode = 0;

	joinSem = new Semaphore("joinsem", 0);
	exitSem = new Semaphore("exitsem", 0);
	multex = new Semaphore("multex", 1);
}

PCB::~PCB()
{
	if (joinSem != NULL)
		delete joinSem;

	if (exitSem != NULL)
		delete exitSem;

	if (multex != NULL)
		delete multex;

	// giai phong tien trinh khoi bo nho
	if (m_thread != NULL)
	{
		m_thread->FreeSpace();
		m_thread->Finish();
	}
}

int PCB::GetExitCode()
{
	return this->exitcode;
}

void PCB::SetExitCode(int ec)
{
	this->exitcode = ec;
}

char *PCB::GetFileName()
{
	return this->filename;
}

void PCB::SetFileName(char *fn)
{
	strcpy(this->filename, fn);
}

int PCB::GetNumWait()
{
	return this->numWait;
}

int PCB::GetID()
{
	return m_thread->processID;
}

void PCB::JoinRelease()
{
	// giai phong va cho phep tien trinh chay
	joinSem->V();
}

void PCB::JoinWait()
{
	// bat tien trinh phai wait khi join, chi chay khi thuc hien lenh JoinRelease()
	joinSem->P();
}

void PCB::ExitRelease()
{
	// tuong tu nhu join
	exitSem->V();
}

void PCB::ExitWait()
{
	// tuong tu nhu join
	exitSem->P();
}

void PCB::DecNumWait()
{
	// doi den khi duoc thuc hien
	multex->P();
	// tien hanh giam so luong wait
	// chua co tien trinh nao wait the nen khong giam so luong wait xuong duoc
	if (numWait > 0)
		--numWait;
	// giai phong tien trinh
	multex->V();
}

void PCB::IncNumWait()
{
	// doi den khi duoc thuc hien
	multex->P();
	// tien hanh tang so luong wait
	++numWait;
	// giai phong tien trinh
	multex->V();
}

int PCB::Exec(char *filename, int pid)
{
	// tranh truong hop nap chong nhieu tien trinh trong luc nap tien trinh
	multex->P();

	// tao thread cho tien trinh
	m_thread = new Thread(filename);

	// khong the tao tien trinh
	if (m_thread == NULL)
	{
		printf("\nERROR: Khong the tao thread");
		multex->V();
		return -1;
	}

	m_thread->processID = pid;			 // dat pid la id cua thread moi tao
	parentID = currentThread->processID; // thread hien tai se la cha cua thread moi tao

	// sau do tien hanh chay thread
	m_thread->Fork(StartProcessNoExec, pid);

	// giai phong semaphore khi da nap tien trinh xong
	multex->V();

	// tra ve ID cua process
	return pid;
}