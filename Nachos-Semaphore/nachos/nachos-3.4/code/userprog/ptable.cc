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

PTable::PTable()
{
	int i;

	psize = MAX_PROCESS;
	bm = new BitMap(psize);
	bmsem = new Semaphore("bmsem", 1);

	for (i = 0; i < MAX_PROCESS; i++)
	{
		pcb[i] = NULL;
	}
}

PTable::PTable(int size)
{
	int i;

	if (size < 0)
	{
		printf("\nERROR: Kich thuoc PTable be hon 0!");
		return;
	}
	else
	{
		psize = size;
		bm = new BitMap(psize);
		bmsem = new Semaphore("bmsem", 1);

		// gan cac process control block ban dau la NULL
		for (i = 0; i < MAX_PROCESS; i++)
		{
			pcb[i] = NULL;
		}
	}
}

PTable::~PTable()
{
	int i;

	if (bm != NULL)
		delete bm;

	if (bmsem != NULL)
		delete bmsem;

	for (i = 0; i < psize; i++)
	{
		if (pcb[i] != NULL)
			delete pcb[i];
	}
}

int PTable::ExecUpdate(char *name)
{
	// tranh truong hop nap chong nhieu tien trinh trong luc nap tien trinh
	bmsem->P();

	// ten khong hop le
	if (name == NULL)
	{
		printf("\nERROR: Ten khong duoc de trong");
		bmsem->V();
		return -1;
	}

	// tranh truong hop process goi lai chinh no
	if (strcmp(name, currentThread->getName()) == 0)
	{
		printf("\nERROR: Process goi lai chinh no!");
		bmsem->V();
		return -1;
	}

	// tim slot trong
	int idx = this->GetFreeSlot();

	// neu khong con slot
	if (idx < 0)
	{
		printf("\nERROR: Khong con slot trong!");
		bmsem->V();
		return -1;
	}

	// danh dau da su dung
	bm->Mark(idx);

	// neu con slot thi tien hanh tao pcb
	pcb[idx] = new PCB(idx);
	pcb[idx]->SetFileName(name);
	pcb[idx]->parentID = currentThread->processID;

	// goi exec cua pcb moi vua tao
	int result = pcb[idx]->Exec(name, idx);

	// giai phong semaphore khi da nap tien trinh xong
	bmsem->V();

	// tra ve ket qua exec cua pcb
	return result;
}

int PTable::ExitUpdate(int ec)
{
	int id = currentThread->processID;

	// chuong trinh main
	if (id == 0)
	{
		// giai phong bo nho
		currentThread->FreeSpace();

		// sau do dung chuong trinh
		interrupt->Halt();
		return 0;
	}

	if (!this->isExist(id))
	{
		printf("\nERROR: Khong ton tai process");
		return -1;
	}
	else
	{
		// dau tien dat exitcode cua process co id hien tai
		pcb[id]->SetExitCode(ec);

		// sau do giam so luong process dang cho cua process cha cua process hien tai
		int parentID = pcb[id]->parentID;
		pcb[parentID]->DecNumWait();

		// tiep theo giai phong tien trinh
		pcb[id]->JoinRelease();
		pcb[id]->ExitWait();

		// xoa process khoi PTable
		this->Remove(id);

		// tra ve ket qua
		return ec;
	}
}

int PTable::JoinUpdate(int id)
{
	// ID khong hop le
	if (id < 0)
	{
		printf("\nERROR: ID khong hop le!");
		return -1;
	}

	// neu ton tai nhung cha khong la process hien tai
	int parentID = pcb[id]->parentID;
	if (currentThread->processID != parentID)
	{
		printf("\nERROR: Process khong hop le!");
		return -1;
	}

	// tang numwait cua tien trinh cha va cho phep tien trinh con join voi tien trinh cha
	pcb[parentID]->IncNumWait();
	pcb[id]->JoinWait();

	// xu ly exit code
	int result = pcb[id]->GetExitCode();
	pcb[id]->ExitRelease();

	return result;
}

int PTable::GetFreeSlot()
{
	// tim trang trong
	return bm->Find();
}

bool PTable::isExist(int pid)
{
	return bm->Test(pid);
}

void PTable::Remove(int pid)
{
	if (!isExist(pid))
		return;

	// xoa id trong bitmap
	bm->Clear(pid);

	// xoa process co id tuong ung ra khoi mang
	delete pcb[pid];
	pcb[pid] = NULL;
}

char *PTable::GetFileName(int id)
{
	if (!isExist(id))
	{
		printf("\nERROR: Khong ton tai process!");
		return NULL;
	}
	return pcb[id]->GetFileName();
}