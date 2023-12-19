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
    for (i = 0; i < MAX_SEMAPHORE; i++)
    {
        semTab[i] = NULL;
    }
}

STable::~STable()
{
    int i;

    delete bm;
    bm = NULL;

    for (i = 0; i < MAX_SEMAPHORE; i++)
    {
        delete semTab[i];
        semTab[i] = NULL;
    }
}

int STable::Create(char *name, int init)
{
    int i;

    // Check da ton tai semaphore nay chua?
    for (i = 0; i < MAX_SEMAPHORE; i++)
    {
        if (bm->Test(i))
        {
            if (strcmp(name, semTab[i]->GetName()) == 0)
            {
                printf("\nERROR: Da ton tai semaphore!");
                return -1;
            }
        }
    }

    // Tim slot tren bang semTab trong
    int id = this->FindFreeSlot();

    // Neu k tim thay thi tra ve -1
    if (id < 0)
    {
        printf("\nERROR: Khong con vi tri trong!");
        return -1;
    }

    // Neu tim thay slot trong thi nap Semaphore vao semTab[id]
    this->semTab[id] = new Sem(name, init);
    return 0;
}

int STable::Wait(char *name)
{
    int i;
    for (i = 0; i < MAX_SEMAPHORE; i++)
    {
        // Kiem tra o thu i da duoc nap semaphore chua
        if (bm->Test(i))
        {
            // Neu co thi tien hanh so sanh name voi name cua semaphore trong semTab
            if (strcmp(name, semTab[i]->GetName()) == 0)
            {
                // Neu ton tai thi cho semaphore down();
                semTab[i]->wait();
                return 0;
            }
        }
    }
    printf("\nERROR: Khong ton tai semaphore!");
    return -1;
}

int STable::Signal(char *name)
{
    int i;
    for (i = 0; i < MAX_SEMAPHORE; i++)
    {
        // Kiem tra o thu i da duoc nap semaphore chua
        if (bm->Test(i))
        {
            // Neu co thi tien hanh so sanh name voi name cua semaphore trong semTab
            if (strcmp(name, semTab[i]->GetName()) == 0)
            {
                // Neu ton tai thi cho semaphore up();
                semTab[i]->signal();
                return 0;
            }
        }
    }
    printf("\nERROR: Khong ton tai semaphore!");
    return -1;
}

int STable::FindFreeSlot()
{
    return this->bm->Find();
}