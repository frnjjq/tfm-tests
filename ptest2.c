/**
 * Test for camera_reader and downsampling integration
 */
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void *t1_task();
void *t2_task();

pthread_t t1, t2;
pthread_mutex_t mutex;
pthread_cond_t cv;
int processed = 0;
int main(int argc, char *argv[])
{
    int status;

    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&cv, NULL);

    status = pthread_create(&t1, NULL, t1_task, (void *)0);
    if (status)
    {
        printf("Error creating thread 1 %d\n", status);
    }
    status = pthread_create(&t2, NULL, t2_task, (void *)0);
    if (status)
    {
        printf("Error creating thread 2 %d\n", status);
    }

    sleep(4);

    status = pthread_cancel(t1);
    if (status)
    {
        printf("Error cancelling thread 1 %d\n", status);
    }
    status = pthread_cancel(t2);
    if (status)
    {
        printf("Error cancelling thread 2 %d\n", status);
    }

    return 0;
}

void *t1_task(void *argument)
{
    sleep(1);
    pthread_mutex_lock(&mutex);
    printf("Me quedo esperando en el t1\n");
    while (processed == 0)
    { // Solo espero si aun no está procesado entonces espero al signal.
        pthread_cond_wait(&cv, &mutex);
    }
    printf("He obtenido el mutex tras esperar en el t1\n");
    processed = 0;
    pthread_mutex_unlock(&mutex);
    pthread_exit(NULL);
}

void *t2_task(void *argument)
{
    pthread_mutex_lock(&mutex);
    processed = 1;            // Proceso lo que me haga falta
    pthread_cond_signal(&cv); // Signaleo por si acaso aun que quizás no este escuchando
    printf("He signaleado en el t2\n");
    pthread_mutex_unlock(&mutex);
    printf("Dejo el mutex en el t2\n");
    pthread_exit(NULL);
}