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
	if (id == 0)
		parentID = -1;
	else
		parentID = currentThread->processID;
	
	// tien trinh van chua duoc chay
	m_thread = NULL;
	
	numWait = 0;
	exitcode = 0;
	
	joinSem = new Semaphore("joinsem", 1);
	exitSem = new Semaphore("exitsem", 1);
	multex = new Semaphore("multex", 1);
}

PCB::~PCB()
{
	delete joinSem;
	delete exitSem;
	delete multex;
	
	// giai phong tien trinh khoi bo nho
	delete m_thread->space;
	
	// hoan thanh chay tien trinh
	m_thread->Finish();
}

int PCB::Exec(char* filename, int pid)
{	
	// tranh truong hop nap chong nhieu tien trinh trong luc nap tien trinh
	multex->P();
	
	// tao thread cho tien trinh
	m_thread = new Thread(filename);
	
	// khong the tao tien trinh
	if (m_thread == NULL)
	{
		DEBUG('a', "\nERROR: Khong the tao Thread!");
		multex->V();
		return -1;
	}
	
	m_thread->processID = pid; // dat pid la id cua thread moi tao
	parentID = currentThread->processID; // thread hien tai se la cha cua thread moi tao
	
	// sau do tien hanh chay thread
	m_thread->Fork(StartProcessNoExec, pid);
	
	// giai phong semaphore khi da nap tien trinh xong
	multex->V();
	
	return 1;
}

int PCB::GetID()
{
	return m_thread->processID;
}

int PCB::GetNumWait()
{
	return numWait;
}

void PCB::JoinWait()
{
	// bat tien trinh phai wait khi join, chi chay khi thuc hien lenh JoinRelease()
	joinSem->P();
}

void PCB::ExitWait()
{
	// tuong tu nhu join
	exitSem->P();
}

void PCB::JoinRelease()
{
	// giai phong va cho phep tien trinh chay
	joinSem->V();
}

void PCB::ExitRelease()
{
	// tuong tu nhu join
	exitSem->V();
}

void PCB::IncNumWait()
{
	// doi den khi duoc thuc hien 
	multex->P();
	// tien hanh tang so luong wait
	numWait++;
	// giai phong tien trinh
	multex->V();
}

void PCB::DecNumWait()
{
	// chua co tien trinh nao wait the nen khong giam so luong wait xuong duoc
	if (numWait == 0)
		return;
	
	// doi den khi duoc thuc hien 
	multex->P();
	// tien hanh giam so luong wait
	numWait--;
	// giai phong tien trinh
	multex->V();
}

void PCB::SetExitCode(int ec)
{
	exitcode = ec;
}

int PCB::GetExitCode()
{
	return exitcode;
}

void PCB::SetFileName(char* fn)
{
	strcpy(filename, fn);
}

char* PCB::GetFileName()
{
	return filename;
}