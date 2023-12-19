// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#ifndef STABLE_H
#define STABLE_H

#include "synch.h"
#include "bitmap.h"

#define MAX_SEMAPHORE 10

// class quan ly semaphore
class Sem
{
public:
	Sem(char *na, int i)
	{
		strcpy(this->name, na);
		sem = new Semaphore(name, i);
	}

	~Sem()
	{
		delete sem;
	}

	// thuc hien thao tac cho
	void wait()
	{
		sem->P();
	}

	// thuc hien thao tac giai phong Semaphore
	void signal()
	{
		sem->V();
	}

	// tra ve ten cua Semaphore
	char *GetName()
	{
		return name;
	}

private:
	// ten cua semaphore
	char name[50];
	// semaphore
	Semaphore *sem;
};

class STable
{
public:
	STable();
	~STable();

	/*
	 * Kiem tra Semaphore "name" co ton tai khong
	 * Neu khong thi tao Semaphore
	 * Nguoc lai thi bao loi
	 */
	int Create(char *name, int init);

	/*
	 * Neu ton tai Semaphore "name" thi goi wait() cua Semaphore tuong ung
	 * Neu khong thi bao loi
	 */
	int Wait(char *name);

	/*
	 * Neu ton tai Semaphore "name" thi goi signal() cua Semaphore tuong ung
	 * Neu khong thi bao loi
	 */
	int Signal(char *name);

	// tim slot trong cho semaphore
	int FindFreeSlot();

private:
	BitMap *bm;					// quan ly slot trong
	Sem *semTab[MAX_SEMAPHORE]; // quan ly toi da 10 doi tuong Sem
};

#endif // STABLE_H