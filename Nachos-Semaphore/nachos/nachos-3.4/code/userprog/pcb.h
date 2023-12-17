// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#ifndef PCB_H
#define PCB_H

#include "thread.h"
#include "synch.h"

class PCB
{
public:
	int parentID; // ID cua tien trinh cha
	
	PCB(int id);
	~PCB();
	
	/*
	 * Nap chuong trinh co ten luu trong bien filename va processID la processID
	 * Sau do tao 1 thread moi ten la filename va processID la pid
	 */
	int Exec(char* filename, int pid);
	
	// tra ve process ID cua tien trinh duoc goi
	int GetID();
	
	// tra ve so luong tien trinh cho
	int GetNumWait();
	
	// 1. Tien trinh cha doi tien trinh con ket thuc
	void JoinWait();
	// 4. Tien trinh con ket thuc
	void ExitWait();
	// 2. Bao cho tien trinh cha thuc thi tiep
	void JoinRelease();
	// 3. Cho phep tien trinh con ket thuc
	void ExitRelease();
	
	// Tang so tien trinh cho
	void IncNumWait();
	// Giam so tien trinh cho
	void DecNumWait();
	
	// Dat exitcode cua tien trinh
	void SetExitCode(int ec);
	// Tra ve exitcode
	int GetExitCode();
	
	// Dat ten cua tien trinh
	void SetFileName(char* fn);
	// Tra ve ten cua tien trinh
	char* GetFileName();
	
private:
	Semaphore* joinSem; // semephore cho qua trinh join
	Semaphore* exitSem; // semaphore cho qua trinh exit
	Semaphore* multex; // semaphore cho qua trinh truy xuat doc quyen
	int exitcode;
	int numWait; // so tien trinh da join
	char filename[50]; // ten cua tien trinh
	Thread* m_thread; // thread cua tien trinh
};

#endif // PBC_H