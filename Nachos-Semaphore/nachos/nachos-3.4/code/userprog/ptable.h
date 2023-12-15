// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#ifndef PTABLE_H
#define PTABLE_H

#include "pcb.h"
#include "bitmap.h"
#include "synch.h"

#define MAX_PROCESS 10

class PTable
{
public:
	/*
	 * Khoi tao size PCB de luu size process. Gan gia tri ban dau la null
	 * Nho khoi tao bm va bmsen de su dung
	 */
	PTable(int size);
	
	// huy cac doi tuong da tao
	~PTable();
	
	// Xu ly cho system call SC_Exit
	int ExecUpdate(char* name);
	
	// Xu ly cho system call SC_Exit
	int ExitUpdate(int ec);
	
	// Xu ly cho system call SC_Join
	int JoinUpdate(int id);
	
	// Tim slot trong de luu tien trinh moi
	int GetFreeSlot();
	
	// Kiem tra co ton tai tien trinh nao voi pid khong
	bool isExist(int pid);
	
	// Khi tien trinh ket thuc, xoa pid cua no ra khoi mang
	void Remove(int pid);
	
	// Tra ve ten cua tien trinh
	char* GetFileName(int id);
	
private:
	BitMap* bm; // danh dau cac vi tri da duoc su dung trong PCB
	PCB* pcb[MAX_PROCESS];
	int psize;
	Semaphore* bmsem; // dun de ngan chan truong hop nap 2 tien trinh cung luc
};

#endif // PTABLE_H