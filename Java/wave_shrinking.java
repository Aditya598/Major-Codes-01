// A wave shrinking algorithm that takes a wave of a certain length greater than 128 and shrinks it down 
// to 128 samples while still retaining the original shape
// The program uses copyrighted code (for fft and ifft) along with the main code  


/*
 * Free FFT and convolution (Java)
 *
 * Copyright (c) 2017 Project Nayuki. (MIT License)
 * https://www.nayuki.io/page/free-small-fft-in-multiple-languages
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of
 * this software and associated documentation files (the "Software"), to deal in
 * the Software without restriction, including without limitation the rights to
 * use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 * the Software, and to permit persons to whom the Software is furnished to do so,
 * subject to the following conditions:
 * - The above copyright notice and this permission notice shall be included in
 *   all copies or substantial portions of the Software.
 * - The Software is provided "as is", without warranty of any kind, express or
 *   implied, including but not limited to the warranties of merchantability,
 *   fitness for a particular purpose and noninfringement. In no event shall the
 *   authors or copyright holders be liable for any claim, damages or other
 *   liability, whether in an action of contract, tort or otherwise, arising from,
 *   out of or in connection with the Software or the use or other dealings in the
 *   Software.
 */

import flanagan.complex.Complex;
import flanagan.math.FourierTransform;

import java.util.*;


public final class Fft {

    /*
     * Computes the discrete Fourier transform (DFT) of the given complex vector, storing the result back into the vector.
     * The vector can have any length. This is a wrapper function.
     */
    public static void transform(double[] real, double[] imag) {
        int n = real.length;
        if (n != imag.length)
            throw new IllegalArgumentException("Mismatched lengths");
        if (n == 0)
            return;
        else if ((n & (n - 1)) == 0)  // Is power of 2
            transformRadix2(real, imag);
        else  // More complicated algorithm for arbitrary sizes
            transformBluestein(real, imag);
    }


    /*
     * Computes the inverse discrete Fourier transform (IDFT) of the given complex vector, storing the result back into the vector.
     * The vector can have any length. This is a wrapper function. This transform does not perform scaling, so the inverse is not a true inverse.
     */
    public static void inverseTransform(double[] real, double[] imag) {
        transform(imag, real);
    }


    /*
     * Computes the discrete Fourier transform (DFT) of the given complex vector, storing the result back into the vector.
     * The vector's length must be a power of 2. Uses the Cooley-Tukey decimation-in-time radix-2 algorithm.
     */
    public static void transformRadix2(double[] real, double[] imag) {
        // Length variables
        int n = real.length;
        if (n != imag.length)
            throw new IllegalArgumentException("Mismatched lengths");
        int levels = 31 - Integer.numberOfLeadingZeros(n);  // Equal to floor(log2(n))
        if (1 << levels != n)
            throw new IllegalArgumentException("Length is not a power of 2");

        // Trigonometric tables
        double[] cosTable = new double[n / 2];
        double[] sinTable = new double[n / 2];
        for (int i = 0; i < n / 2; i++) {
            cosTable[i] = Math.cos(2 * Math.PI * i / n);
            sinTable[i] = Math.sin(2 * Math.PI * i / n);
        }

        // Bit-reversed addressing permutation
        for (int i = 0; i < n; i++) {
            int j = Integer.reverse(i) >>> (32 - levels);
            if (j > i) {
                double temp = real[i];
                real[i] = real[j];
                real[j] = temp;
                temp = imag[i];
                imag[i] = imag[j];
                imag[j] = temp;
            }
        }

        // Cooley-Tukey decimation-in-time radix-2 FFT
        for (int size = 2; size <= n; size *= 2) {
            int halfsize = size / 2;
            int tablestep = n / size;
            for (int i = 0; i < n; i += size) {
                for (int j = i, k = 0; j < i + halfsize; j++, k += tablestep) {
                    int l = j + halfsize;
                    double tpre = real[l] * cosTable[k] + imag[l] * sinTable[k];
                    double tpim = -real[l] * sinTable[k] + imag[l] * cosTable[k];
                    real[l] = real[j] - tpre;
                    imag[l] = imag[j] - tpim;
                    real[j] += tpre;
                    imag[j] += tpim;
                }
            }
            if (size == n)  // Prevent overflow in 'size *= 2'
                break;
        }
    }


    /*
     * Computes the discrete Fourier transform (DFT) of the given complex vector, storing the result back into the vector.
     * The vector can have any length. This requires the convolution function, which in turn requires the radix-2 FFT function.
     * Uses Bluestein's chirp z-transform algorithm.
     */
    public static int[] transformBluestein(double[] real, double[] imag) {
        // Find a power-of-2 convolution length m such that m >= n * 2 + 1
        double max_original, min_original;
        max_original = min_original = real[0];
        int n = real.length;
        if (n != imag.length)
            throw new IllegalArgumentException("Mismatched lengths");
        if (n >= 0x20000000)
            throw new IllegalArgumentException("Array too large");
        int m = Integer.highestOneBit(n) * 4;

        // Trignometric tables
        double[] cosTable = new double[n];
        double[] sinTable = new double[n];

        for (int i = 0; i < real.length; i++) {
            max_original = Math.max(max_original, real[i]);
            min_original = Math.min(min_original, real[i]);
        }

        for (int i = 0; i < n; i++) {
            int j = (int) ((long) i * i % (n * 2));  // This is more accurate than j = i * i
            cosTable[i] = Math.cos(Math.PI * j / n);
            sinTable[i] = Math.sin(Math.PI * j / n);
        }

        // Temporary vectors and preprocessing
        double[] areal = new double[m];
        double[] aimag = new double[m];
        for (int i = 0; i < n; i++) {
            areal[i] = real[i] * cosTable[i] + imag[i] * sinTable[i];
            aimag[i] = -real[i] * sinTable[i] + imag[i] * cosTable[i];
        }
        double[] breal = new double[m];
        double[] bimag = new double[m];
        breal[0] = cosTable[0];
        bimag[0] = sinTable[0];
        for (int i = 1; i < n; i++) {
            breal[i] = breal[m - i] = cosTable[i];
            bimag[i] = bimag[m - i] = sinTable[i];
        }

        // Convolution
        double[] creal = new double[m];
        double[] cimag = new double[m];
        convolve(areal, aimag, breal, bimag, creal, cimag);

        // Postprocessing
        for (int i = 0; i < n; i++) {
            real[i] = creal[i] * cosTable[i] + cimag[i] * sinTable[i];
            imag[i] = -creal[i] * sinTable[i] + cimag[i] * cosTable[i];
        }


        Complex dataForIFFT[] = new Complex[128];
        for (int i = 0; i < 128; i++) dataForIFFT[i] = new Complex(0, 0);
        int i1 = 0;

        try {

            for (i1 = 0; i1 < 128; i1++) {
                dataForIFFT[i1].setReal(real[i1]);
                dataForIFFT[i1].setImag(imag[i1]);
            }
        } catch (NullPointerException e) {
            System.out.println("i = " + i1);
        }

        FourierTransform ft = new FourierTransform(dataForIFFT);
        ft.inverse();
        Complex dataAfterIFFT[] = ft.getTransformedDataAsComplex();

        double IFFTReal[] = new double[128];

        for (int i = 0; i < 128; i++) IFFTReal[i] = dataAfterIFFT[i].getReal();

        int reverse_array[] = new int[128];
        for (int i = 0; i < 128; i++) reverse_array[128 - i - 1] = (int)IFFTReal[i];

        /*System.out.println();
        System.out.println("128 data after ifft:");
        for(int i = 0; i < 128; i++) System.out.println(reverse_array[i]);
        System.out.println();*/

        double shifted_real2[] = shifting2(IFFTReal, max_original, min_original);

        int reverse_shifted_array2[] = new int[128];

        for (int i = 0; i < 128; i++) reverse_shifted_array2[128 - i - 1] = (int) Math.round(shifted_real2[i]);

        return reverse_shifted_array2;

    }


    /*
     * Computes the circular convolution of the given real vectors. Each vector's length must be the same.
     */
    public static void convolve(double[] x, double[] y, double[] out) {
        int n = x.length;
        if (n != y.length || n != out.length)
            throw new IllegalArgumentException("Mismatched lengths");
        convolve(x, new double[n], y, new double[n], out, new double[n]);
    }


    /*
     * Computes the circular convolution of the given complex vectors. Each vector's length must be the same.
     */
    public static void convolve(double[] xreal, double[] ximag,
                                double[] yreal, double[] yimag, double[] outreal, double[] outimag) {

        int n = xreal.length;
        if (n != ximag.length || n != yreal.length || n != yimag.length
                || n != outreal.length || n != outimag.length)
            throw new IllegalArgumentException("Mismatched lengths");

        xreal = xreal.clone();
        ximag = ximag.clone();
        yreal = yreal.clone();
        yimag = yimag.clone();
        transform(xreal, ximag);
        transform(yreal, yimag);

        for (int i = 0; i < n; i++) {
            double temp = xreal[i] * yreal[i] - ximag[i] * yimag[i];
            ximag[i] = ximag[i] * yreal[i] + xreal[i] * yimag[i];
            xreal[i] = temp;
        }
        inverseTransform(xreal, ximag);

        for (int i = 0; i < n; i++) {  // Scaling (because this FFT implementation omits it)
            outreal[i] = xreal[i] / n;
            outimag[i] = ximag[i] / n;
        }
    }

    public static void main(String[] args) {

        Scanner s = new Scanner(System.in);
        System.out.println("Enter data");
        ArrayList<Integer> data = new ArrayList<>();
        ArrayList<String> data2Print = new ArrayList<>();

        boolean pass = true;
        double reals[], zeros[];

        int transformed_Wave[] = new int[128];

        int sample, count = 0;

        while (true) {

            count++;


            for (; true; ) {

                sample = s.nextInt();
                if (sample < 0) {
                    if (sample == -2) pass = false;
                    break;
                } else {
                    data.add(sample);
                }
            }

            zeros = new double[data.size()];
            reals = new double[data.size()];
            for (int i = 0; i < data.size(); i++) zeros[i] = 0;
            for (int i = 0; i < data.size(); i++) reals[i] = data.get(i);

            double original_data[] = new double[reals.length];

            for (int i = 0; i < reals.length; i++) {
                original_data[i] = reals[i];
            }

            if (original_data.length != 128) transformed_Wave = transformBluestein(original_data, zeros);
            else {
                for (int i = 0; i < 128; i++) transformed_Wave[i] = (int) original_data[i];
            }

            for (int i = 0; i < reals.length; i++) {

                if (count == 1) {
                    if (i == 0) data2Print.add("Original Wave " + count + "\tTransformed Wave " + count + "\t");
                    else {
                        if (i < 129) data2Print.add(Math.round(reals[i-1]) + "\t" + transformed_Wave[i-1] + "\t");
                        else data2Print.add(Math.round(reals[i-1]) + "\t\t");
                    }
                } else {
                    if (i == 0)
                        data2Print.set(i, data2Print.get(i) + "Original Wave " + count + "\tTransformed Wave " + count + "\t");
                    else {
                        if (i < 129)
                            data2Print.set(i, data2Print.get(i) + Math.round(reals[i-1]) + "\t" + transformed_Wave[i-1] + "\t");
                        else if (i > (data2Print.size()-1)) data2Print.add(Math.round(reals[i-1]) + "\t\t");
                        else data2Print.set(i, data2Print.get(i) + Math.round(reals[i-1]) + "\t\t");
                    }

                }
            }


            if (!pass) {
                for (int i = 0; i < data2Print.size(); i++) System.out.println(data2Print.get(i));
                break;
            } else {
                data.clear();
            }
        }
    }


    static double[] shifting2(double mat[], double max_og, double min_og) {

        double max, min;
        double shifted_matrix[] = new double[128];
        double final_matrix[] = new double[128];

        int flatStart = 0, flatEnd = 0;

        max = min = mat[0];
        for (int i = 0; i < mat.length; i++) {
            max = Math.max(mat[i], max);
            min = Math.min(mat[i], min);
        }


        for (int i = 1; i < mat.length; i++) {
            if ((Math.abs(mat[i] - mat[i - 1]) < 5) && (mat[i] > ((max - min) / 2 + min - 50) && mat[i] < ((max - min) / 2 + min + 50))) {
                if (flatStart == 0) flatStart = i - 1;
                else flatEnd = i;
            }
        }

        double midpoint = (mat[flatStart] + mat[flatEnd]) / 2, original_midpoint = 512;

        if ((flatStart == 0 && flatEnd == 0)) midpoint = (max - min) / 2 + min;

        if (midpoint > original_midpoint) {
            max -= (midpoint - original_midpoint);
            min -= (midpoint - original_midpoint);
        } else {
            max += (midpoint - original_midpoint);
            min += (midpoint - original_midpoint);
        }

        for (int i = 0; i < mat.length; i++) {
            if (midpoint > original_midpoint) shifted_matrix[i] = mat[i] - (midpoint - original_midpoint);
            else shifted_matrix[i] = mat[i] + (original_midpoint - midpoint);

            if (shifted_matrix[i] > original_midpoint)
                final_matrix[i] = (shifted_matrix[i] - original_midpoint) * ((max_og - original_midpoint) / (max - original_midpoint)) + original_midpoint;
            else if (shifted_matrix[i] < original_midpoint)
                final_matrix[i] = (shifted_matrix[i] - original_midpoint) * ((min_og - original_midpoint) / (min - original_midpoint)) + original_midpoint;

            //final_matrix[i] = Math.min(1023,final_matrix[i]);
            //final_matrix[i] = Math.max(0,final_matrix[i]);
        }

        return final_matrix;
    }

}
