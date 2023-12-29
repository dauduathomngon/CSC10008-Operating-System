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
		this->parentID = -1;
	else
		this->parentID = currentThread->processID;

	this->numwait = this->exitcode = this->boolBG = 0;
	this->m_thread = NULL;

	this->joinsem = new Semaphore("joinsem", 0);
	this->exitsem = new Semaphore("exitsem", 0);
	this->multex = new Semaphore("multex", 1);
}

PCB::~PCB()
{

	if (joinsem != NULL)
		delete this->joinsem;
	if (exitsem != NULL)
		delete this->exitsem;
	if (multex != NULL)
		delete this->multex;
	if (m_thread != NULL)
	{
		m_thread->FreeSpace();
		m_thread->Finish();
	}
}

int PCB::GetID()
{
	return this->m_thread->processID;
}

int PCB::GetNumWait()
{
	return this->numwait;
}

int PCB::GetExitCode()
{
	return this->exitcode;
}

void PCB::SetExitCode(int ec)
{
	this->exitcode = ec;
}

void PCB::JoinWait()
{
	// Gọi joinsem->P() để tiến trình chuyển sang trạng thái block và ngừng lại, chờ JoinRelease để thực hiện tiếp.
	joinsem->P();
}

void PCB::JoinRelease()
{
	// Gọi joinsem->V() để giải phóng tiến trình gọi JoinWait().
	joinsem->V();
}

void PCB::ExitWait()
{
	// Gọi exitsem-->V() để tiến trình chuyển sang trạng thái block và ngừng lại, chờ ExitReleaseđể thực hiện tiếp.
	exitsem->P();
}

void PCB::ExitRelease()
{
	// Gọi exitsem-->V() để giải phóng tiến trình đang chờ.
	exitsem->V();
}

void PCB::IncNumWait()
{
	multex->P();
	++numwait;
	multex->V();
}

void PCB::DecNumWait()
{
	multex->P();
	if (numwait > 0)
		--numwait;
	multex->V();
}

void PCB::SetFileName(char *fn)
{
	strcpy(FileName, fn);
}

char *PCB::GetFileName()
{
	return this->FileName;
}

int PCB::Exec(char *filename, int id)
{
	// Gọi mutex->P(); để giúp tránh tình trạng nạp 2 tiến trình cùng 1 lúc.
	multex->P();

	// Kiểm tra m_thread đã khởi tạo thành công chưa, nếu chưa thì báo lỗi là không đủ bộ nhớ, gọi mutex->V() và return.
	this->m_thread = new Thread(filename);

	if (this->m_thread == NULL)
	{
		printf("\nERROR: Khong du bo nho!\n");
		multex->V();
		return -1;
	}

	// Đặt processID của m_thread này là id.
	this->m_thread->processID = id;
	// Đặt parrentID của m_thread này là processID của m_thread gọi thực thi Exec
	this->parentID = currentThread->processID;
	// Gọi thực thi Fork(StartProcessNoExec,id) => Ta cast m_thread thành kiểu int
	// sau đó khi xử lý hàm StartProcess ta cast Thread về đúng kiểu của nó.
	this->m_thread->Fork(StartProcessNoExec, id);

	multex->V();
	// Trả về id.
	return id;
}
