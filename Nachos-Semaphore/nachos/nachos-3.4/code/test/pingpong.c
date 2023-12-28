// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------

#include "syscall.h"

int main()
{
	int pingID;
	int pongID;
	int semPong;
	int semPing;

	PrintString("Test chuong trinh Ping Pong:\n\n");

	// tao 2 semaphore
	semPing = CreateSemaphore("ping", 1);
	semPong = CreateSemaphore("pong", 0);

	// tao 2 tien trinh
	pingID = Exec("./test/ping");
	pongID = Exec("./test/pong");

	// cho 2 tien trinh chay xen ke nhau
	Join(pingID);
	Join(pongID);
}