// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#include "ptable.h"
#include "system.h"
#include "openfile.h"

PTable::PTable(int size)
: psize(size)
{
	int i;
	
	if (psize < 0)
		return;

	bm = new BitMap(psize);
	bmsem = new Semaphore("bmsem", 1);
	
	for (i=0; i < MAX_PROCESS; i++)
	{
		pcb[i] = NULL;
	}
	
	bm->Mark(0);
	
	// con thieu doan tao PCB
}

PTable::~PTable()
{
	int i;
	
	delete bm;
	delete bmsem;
	
	for (i=0; i < psize; i++)
	{
		delete pcb[i];
	}
}

int PTable::ExecUpdate(char* name)
{
	return 0;
}

int PTable::ExitUpdate(int ec)
{
	return 0;
}

int PTable::JoinUpdate(int id)
{
	return 0;
}

int PTable::GetFreeSlot()
{
	return 0;
}

bool PTable::isExist(int pid)
{
	return false;
}

void PTable::Remove(int pid)
{

}

char* PTable::GetFileName(int id)
{
	return NULL;
}