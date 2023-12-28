// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#include "stable.h"

STable::STable()
{
	this->bm = new BitMap(MAX_SEMAPHORE);

	for (int i = 0; i < MAX_SEMAPHORE; i++)
	{
		this->semList[i] = NULL;
	}
}

STable::~STable()
{
	if (this->bm)
	{
		delete this->bm;
		this->bm = NULL;
	}

	for (int i = 0; i < MAX_SEMAPHORE; i++)
	{
		if (this->semList[i])
		{
			delete this->semList[i];
			this->semList[i] = NULL;
		}
	}
}

int STable::Create(char *name, int init)
{
	// Check xem semaphore ton tai hay khong ?
	for (int i = 0; i < MAX_SEMAPHORE; i++)
	{
		if (bm->Test(i))
		{
			if (strcmp(name, semList[i]->GetName()) == 0)
			{
				return -1;
			}
		}
	}

	// Tim slot trong
	int id = this->FindFreeSlot();

	// Neu khong co slot trong
	if (id < 0)
	{
		return -1;
	}

	// Neu co thi tao moi semaphore tai slot trong do
	this->semList[id] = new SemList(name, init);
	return 0;
}

int STable::Wait(char *name)
{
	for (int i = 0; i < MAX_SEMAPHORE; i++)
	{
		// Xem vi tri i co semaphore chua
		if (bm->Test(i))
		{
			// So sanh ten semaphore da co voi nam
			if (strcmp(name, semList[i]->GetName()) == 0)
			{
				semList[i]->wait();
				return 0;
			}
		}
	}
	printf("\nERROR: Khong ton tai semaphore");
	return -1;
}

int STable::Signal(char *name)
{
	for (int i = 0; i < MAX_SEMAPHORE; i++)
	{
		if (bm->Test(i))
		{
			if (strcmp(name, semList[i]->GetName()) == 0)
			{
				semList[i]->signal();
				return 0;
			}
		}
	}
	printf("\nERROR: Khong ton tai semaphore");
	return -1;
}

int STable::FindFreeSlot()
{
	return this->bm->Find();
}
