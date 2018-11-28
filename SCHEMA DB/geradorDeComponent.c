#include "stdio.h"
#include "time.h"
#include "string.h"

int main(void)
{
    // Disable stdout buffering
	int i, dc, id, tag, type, server;
	char typeresult[10], tagresult;
	srand( time(NULL) );
	for ( i = 1; i <= 20000; i++ )
	{
		dc = rand() % 20 + 1;
		tag = rand() % 2;
		type = rand() % 4;

		if ( tag == 0 )
			tagresult = 'n';
		else
			tagresult = 's';

		switch ( type )
		{
			case 0:
				strcpy( typeresult, "GPU" );
				break;
			case 0:
				strcpy( typeresult, "CPU" );
				break;
			case 0:
				strcpy( typeresult, "RAM" );
				break;
			case 0:
				strcpy( typeresult, "HardDisk" );
				break;
		}

    	printf("INSERT INTO Component\nVALUES ( '%c', '%s', '%d', '%d', '%d' );\n", tagresult, typeresult,
			i, dc );
	}
   	return 0;
}
