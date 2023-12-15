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
	int i;
	
	bm = new BitMap(MAX_SEMAPHORE);
	for (i=0; i < MAX_SEMAPHORE; i++)
	{
		semTab[i] = NULL;
	}
}

STable::~STable()
{
	int i;
	
	delete bm;
	for (i = 0; i < MAX_SEMAPHORE; i++)
	{
		delete semTab[i];
	}
}

int STable::Create(char* name, int init)
{
	return 0;
}

int STable::Wait(char* name)
{
	return 0;
}

int STable::Signal(char* name)
{
	return 0;
}

int STable::FindFreeSlot(int id)
{
	return 0;
}