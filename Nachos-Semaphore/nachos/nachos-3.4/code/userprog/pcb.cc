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

PCB::PCB()
{
	
}

PCB::PCB(int id)
{
	
}

PCB::~PCB()
{
	
}

int PCB::Exec(char* filename, int pid)
{
	 return 0;
}

int PCB::GetID()
{
	return 0;
}

int PCB::GetNumWait()
{
	return 0;
}

void PCB::JoinWait()
{
	
}

void PCB::ExitWait()
{
	
}

void PCB::JoinRelease()
{
	
}

void PCB::ExitRelease()
{
	
}

void PCB::IncNumWait()
{

}

void PCB::DecNumWait()
{

}

void PCB::SetExitCode(int ec)
{

}

int PCB::GetExitCode()
{
	return 0;
}

void PCB::SetFileName(char* fn)
{

}

char* PCB::GetFileName()
{
	return NULL;
}