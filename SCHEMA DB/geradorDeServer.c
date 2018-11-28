#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>


#define Num_of_Server 2000
#define Num_of_Clients 6

int main(void)
{
    // Disable stdout buffering
	int dc, i, j, compnum = 0;
	int matrizServer[2000];
	char typeresult[10], tagresult;

	FILE *saida;
	saida = fopen( "pop.sql", "w" );
	char clients[Num_of_Clients][10];
	strcpy( clients[0], "192303" );
	strcpy( clients[1],	"19212");
	strcpy( clients[2], "192300");
	strcpy( clients[3],	"321901");
	strcpy( clients[4],	"12392");
	strcpy( clients[5],	"84012");

	if( saida == NULL )
	{
		printf ( "treta detectada!" );
		return -1;
	}

	srand( time(NULL) );
	for ( i = 1; i <= Num_of_Server; i++ )
	{
		dc = rand() % 20 + 1;
		matrizServer[i-1] = dc;
    	fprintf( saida, "INSERT INTO Server\nVALUES ( '%d', '%d' );\n", i, dc );
	}


	printf("\n\n=====================QUERY DE CRIAR COMPONENTE=====================\n\n" );

	for ( i = 1; i <= Num_of_Server; i++ )
	{
		tagresult = 's';
		for ( j = 0; j < 4; j++ )
		{
			compnum++;
			switch ( j )
			{
				case 0:
					strcpy( typeresult, "GPU" );
					break;
				case 1:
					strcpy( typeresult, "CPU" );
					break;
				case 2:
					strcpy( typeresult, "RAM" );
					break;
				case 3:
					strcpy( typeresult, "HardDisk" );
					break;
			}

			fprintf(saida, "INSERT INTO Component\nVALUES ( '%s', '%d', '%d', '%d' );\n", typeresult,
				compnum, i, matrizServer[i-1] );
		}
	}

	printf("\n\n=====================QUERY DE CRIAR COMPONENTE NAO ALOCADO=====================\n\n" );
	for ( i = Num_of_Server + 1; i <= Num_of_Server * 3; i++ )
	{
		dc = rand() % 20 + 1;
		j = rand() % 4;
		tagresult = 'n';
		compnum++;
		switch ( j )
		{
			case 0:
				strcpy( typeresult, "GPU" );
				break;
			case 1:
				strcpy( typeresult, "CPU" );
				break;
			case 2:
				strcpy( typeresult, "RAM" );
				break;
			case 3:
				strcpy( typeresult, "HardDisk" );
				break;
		}
		fprintf( saida, "INSERT INTO Component\nVALUES ( '%s', '%d', %s, '%d' );\n", typeresult,
			compnum, "null", dc );
	}
	fclose( saida );
   	return 0;
	for (  i = 1; i <= Num_of_Server; i++ )
	{
		dc = rand() % Num_of_Clients;
		fprintf( saida, "INSERT INTO Rents\nVALUES( '%s', '%d' )\n", clients[dc], i );
	}
}
