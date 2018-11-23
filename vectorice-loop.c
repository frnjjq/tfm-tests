// gcc -Wall -Wextra -O2 -ftree-vectorize -march=native -fopt-info-vec -fopt-info-vec-missed   -c -o vectorice-loop.o vectorice-loop.c

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{
    int height = 1080, width = 1920;
    //uint8_t raw_data[height* width];
    uint8_t * restrict raw_data = aligned_alloc(64, height* width);
    //uint8_t rgb_data[height* width*3];
    uint8_t * restrict r_data_odd = aligned_alloc(64, height* width);
    uint8_t * restrict g_data_odd = aligned_alloc(64, height* width);
    uint8_t * restrict b_data_odd = aligned_alloc(64, height* width);
    uint8_t * restrict r_data_even = aligned_alloc(64, height* width);
    uint8_t * restrict g_data_even = aligned_alloc(64, height* width);
    uint8_t * restrict b_data_even = aligned_alloc(64, height* width);
    uint8_t * restrict rgb_data = aligned_alloc(64, height* width*3);

    for (int y = 1; y< height-1; y+=2)
    {
        for (int x = 1; x< width; x++) // Valid for odd columns
        {
            r_data_odd[y*width+x] = raw_data[y*width+x];
            g_data_odd[y*width+x] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x] + raw_data[y*width+x+1] +raw_data[y*width+x-1])/4;
            b_data_odd[y*width+x] = (raw_data[(y-1)*width+x-1] + raw_data[(y+1)*width+x+1] + raw_data[(y-1)*width+x+1] +raw_data[(y+1)*width+x-1])/4;
        }
    }
    for (int y = 2; y< height-1; y+=2)
    {
        for (int x = 1; x< width-1; x++) // Valid for odd columns
        {
            r_data_odd[y*width+x] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x])/2;
            g_data_odd[y*width+x] = raw_data[y*width+x];
            b_data_odd[y*width+x] = (raw_data[y*width+x+1] + raw_data[y*width+x-1])/2;
        }
    }
    for (int y = 1; y< height-1; y+=2)
    {
        for (int x = 2; x< width-1; x++) //Even column
        {
            r_data_even[y*width+x] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x])/2;
            g_data_even[y*width+x] = raw_data[y*width+x];
            b_data_even[y*width+x] = (raw_data[y*width+x+1] + raw_data[y*width+x-1])/2;
        }
    }
    for (int y = 2; y< height-1; y+=2)
    {
        for (int x = 2; x< width-1; x++) //Even column and even row
        {
            r_data_even[y*width+x] = (raw_data[(y-1)*width+x-1] + raw_data[(y+1)*width+x+1] + raw_data[(y-1)*width+x+1] +raw_data[(y+1)*width+x-1])/4;
            g_data_even[y*width+x] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x] + raw_data[y*width+x+1] +raw_data[y*width+x-1])/4;
            b_data_even[y*width+x] = raw_data[y*width+x];
        }
    }
    for (int x = 0; x< width-1; x++)
    {
        for (int y = 0; y< height-1; y+=2)
        {
            rgb_data[3*(y*width+x)] = r_data_even[y*width+x];
            rgb_data[3*(y*width+x)+1] = g_data_even[y*width+x];
            rgb_data[3*(y*width+x)+2] = b_data_even[y*width+x];
        }
        for (int y = 1; y< height-1; y+=2)
        {
            rgb_data[3*(y*width+x)] = r_data_odd[y*width+x];
            rgb_data[3*(y*width+x)+1] = g_data_odd[y*width+x];
            rgb_data[3*(y*width+x)+2] = b_data_odd[y*width+x];
        }
    }

    /*for (int y = 1; y< height-1; y+=2)
    {
        for (int x = 1; x< width-1; x+=2) // Odd column and Odd row
        {
            rgb_data[3*(y*width+x)] = raw_data[y*width+x];
            rgb_data[3*(y*width+x)+1] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x] + raw_data[y*width+x+1] +raw_data[y*width+x-1])/4;
            rgb_data[3*(y*width+x)+2] = (raw_data[(y-1)*width+x-1] + raw_data[(y+1)*width+x+1] + raw_data[(y-1)*width+x+1] +raw_data[(y+1)*width+x-1])/4;
        }
    }
    for (int y = 2; y< height-1; y+=2)
    {
        for (int x = 2; x< width-1; x+=2) //Even column and even row
        {
            rgb_data[3*(y*width+x)] = (raw_data[(y-1)*width+x-1] + raw_data[(y+1)*width+x+1] + raw_data[(y-1)*width+x+1] +raw_data[(y+1)*width+x-1])/4;
            rgb_data[3*(y*width+x)+1] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x] + raw_data[y*width+x+1] +raw_data[y*width+x-1])/4;
            rgb_data[3*(y*width+x)+2] = raw_data[y*width+x];
        }
    }
    for (int y = 2; y< height-1; y+=2)
    {
        for (int x = 1; x< width-1; x+=2) //Even column and even row
        {
            rgb_data[3*(y*width+x)] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x])/2;
            rgb_data[3*(y*width+x)+1] = raw_data[y*width+x];
            rgb_data[3*(y*width+x)+2] =  (raw_data[y*width+x+1] + raw_data[y*width+x-1])/2;
        }
    }
    for (int y = 1; y< height-1; y+=2)
    {
        for (int x = 2; x< width-1; x+=2) //Even column and even row
        {
            rgb_data[3*(y*width+x)] = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x])/2;
            rgb_data[3*(y*width+x)+1] = raw_data[y*width+x];
            rgb_data[3*(y*width+x)+2] =  (raw_data[y*width+x+1] + raw_data[y*width+x-1])/2;
        }
    }
    */
/*
    for (int y = 1; y< height-1; y++)
    {
        for (int x = 1; x< width-1; x++)
        {
            if(y%2==0 && x%2==0) // Even column and even row
            {
                r = (raw_data[(y-1)*width+x-1] + raw_data[(y+1)*width+x+1] + raw_data[(y-1)*width+x+1] +raw_data[(y+1)*width+x-1])/4;
                g = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x] + raw_data[y*width+x+1] +raw_data[y*width+x-1])/4;
                b = raw_data[y*width+x];
            }
            else if (y%2!=0 && x%2!=0) // Odd column and Odd row
            {
                r = raw_data[y*width+x];
                g = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x] + raw_data[y*width+x+1] +raw_data[y*width+x-1])/4;
                b = (raw_data[(y-1)*width+x-1] + raw_data[(y+1)*width+x+1] + raw_data[(y-1)*width+x+1] +raw_data[(y+1)*width+x-1])/4;
            }
            else if (y%2==0 && x%2!=0) 
            {
                r = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x])/2;
                g = raw_data[y*width+x];
                b =  (raw_data[y*width+x+1] + raw_data[y*width+x-1])/2;
            }
            else
            {
                r = (raw_data[y*width+x+1] + raw_data[y*width+x-1])/2;
                g = raw_data[y*width+x];
                b = (raw_data[(y-1)*width+x] + raw_data[(y+1)*width+x])/2;
            }
            rgb_data[3*(y*width+x)] = r;
            rgb_data[3*(y*width+x)+1] = g;
        }
    }
    */
    for (int i = 0 ; i< height* width*3; i++)
        printf("whateverr%d %d %d", r_data_odd[i], g_data_odd[i], b_data_odd[i]);
}