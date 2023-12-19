// filesys.h 
//	Data structures to represent the Nachos file system.
//
//	A file system is a set of files stored on disk, organized
//	into directories.  Operations on the file system have to
//	do with "naming" -- creating, opening, and deleting files,
//	given a textual file name.  Operations on an individual
//	"open" file (read, write, close) are to be found in the OpenFile
//	class (openfile.h).
//
//	We define two separate implementations of the file system. 
//	The "STUB" version just re-defines the Nachos file system 
//	operations as operations on the native UNIX file system on the machine
//	running the Nachos simulation.  This is provided in case the
//	multiprogramming and virtual memory assignments (which make use
//	of the file system) are done before the file system assignment.
//
//	The other version is a "real" file system, built on top of 
//	a disk simulator.  The disk is simulated using the native UNIX 
//	file system (in a file named "DISK"). 
//
//	In the "real" implementation, there are two key data structures used 
//	in the file system.  There is a single "root" directory, listing
//	all of the files in the file system; unlike UNIX, the baseline
//	system does not provide a hierarchical directory structure.  
//	In addition, there is a bitmap for allocating
//	disk sectors.  Both the root directory and the bitmap are themselves
//	stored as files in the Nachos file system -- this causes an interesting
//	bootstrap problem when the simulated disk is initialized. 
//
// Copyright (c) 1992-1993 The Regents of the University of California.
// All rights reserved.  See copyright.h for copyright notice and limitation 
// of liability and disclaimer of warranty provisions.

#ifndef FS_H
#define FS_H

#include "copyright.h"
#include "openfile.h"

#ifdef FILESYS_STUB 		// Temporarily implement file system calls as 
				// calls to UNIX, until the real file system
				// implementation is available
class FileSystem {
// ---------------------------------------------
// Thanh vien nhom:
// 21120518 - Dang An Nguyen
// 21120312 - Phan Nguyen Phuong
// 21120498 - Do Hoang Long
// 21120355 - Nguyen Anh Tu
// 21120511 - Le Nguyen
// ---------------------------------------------
public:
	// bang mo ta file (gom 15 phan tu)
	// kiem tra xem file co dang mo khong
	OpenFile* openf[15];
	int index;
	
	FileSystem(bool format)
	{
		index = 0;
		
		int i;
		for (i = 0; i < 15; i++)
		{
			openf[i] = NULL;
		}
		
		// nhap tu console (input)
		this->Create("stdin", 0);
		
		// xuat ra console (output)
		this->Create("stdout", 0);
		
		// vi tri 0 la input
		openf[index++] = this->Open("stdin", 2);
		// vi tri 1 la output
		openf[index++] = this->Open("stdout", 3);
		
		// bat dau tu vi tri 2 la cac file khac
	}
	
	~FileSystem()
	{
		int i;
		for (i = 0; i < 15; i++)
		{
			delete openf[i];
		}
	}
	
	// tao file voi size = initialSize
	bool Create(char* name, int initialSize)
	{
		int fileDescriptor = OpenForWrite(name);
		if (fileDescriptor == -1)
		{
			printf("\nERROR: Khong the tao file\n");
			return FALSE;
		}
		Close(fileDescriptor);
		return TRUE;
	}
	
	// mo file mac dinh
	OpenFile* Open(char* name)
	{
		int fileDescriptor = OpenForReadWrite(name, FALSE);
		if (fileDescriptor == -1)
		{
			printf("\nERROR: Khong the mo file\n");
			return FALSE;
		}
		return new OpenFile(fileDescriptor);
	}
	
	// mo file voi type
	OpenFile* Open(char* name, int type)
	{
		int fileDescriptor = OpenForReadWrite(name, FALSE);
		if (fileDescriptor == -1)
		{
			printf("\nERROR: Khong the mo file\n");
			return FALSE;
		}
		return new OpenFile(fileDescriptor, type);
	}
	
	// tim slot trong
	int FindFreeSlot()
	{
		int i;
		for (i = 2; i < 15; i++)
		{
			// con vi tri trong
			if (openf[i] == NULL)
				return i;
		}
		// khong con vi tri trong
		return -1;
	}
	
	// xoa file khoi bang mo ta
	bool Remove(char* name)
	{
		return Unlink(name) == 0;
	}
};

#else // FILESYS
class FileSystem {
  public:
	  OpenFile* openf[15];
	  int index;
	  
    FileSystem(bool format);		// Initialize the file system.
					// Must be called *after* "synchDisk" 
					// has been initialized.
    					// If "format", there is nothing on
					// the disk, so initialize the directory
    					// and the bitmap of free blocks.

    bool Create(char *name, int initialSize);  	
					// Create a file (UNIX creat)

    OpenFile* Open(char *name); 	// Open a file (UNIX open)
    
    OpenFile* Open(char *name, int type);

    bool Remove(char *name);  		// Delete a file (UNIX unlink)

    void List();			// List all the files in the file system

    void Print();			// List all the files and their contents
	
	int FindFreeSlot();

  private:
   OpenFile* freeMapFile;		// Bit map of free disk blocks,
					// represented as a file
   OpenFile* directoryFile;		// "Root" directory -- list of 
					// file names, represented as a file
};

#endif // FILESYS

#endif // FS_H
