// Input signal elongation using interpolation and smoothing of the elongated signal.


import java.util.*;

import flan

public class signal_processing {
    int originalSamples[];
    Scanner scan = new Scanner(System.in);

    public static void main(String[] args) {

        signal_processing obj = new signal_processing();

           obj.accept_input();
           obj.interpolation();

    }

    void accept_input(){
        ArrayList<Integer> input_wave = new ArrayList<>();
        System.out.println("enter input Data:");
        while (true) {
            int x = scan.nextInt();
            if (x == -10) break;
            input_wave.add(x);
        }
        originalSamples = new int[input_wave.size()];
        for (int i = 0; i < input_wave.size(); i++) {
            originalSamples[i] = input_wave.get(i);
            //System.out.println(a[i]);
        }
    }

    void interpolation(){
        int interpolateFactor = 0;
        double b[];
        double smooth_b[];
        double smoothing_coefficient;

        for(int i = 0;true;i++)
        {
            if((originalSamples.length*i)>128){
                interpolateFactor = i;
                break;
            }
        }


        int elongatedSequenceSize = originalSamples.length*interpolateFactor;

        System.out.println("Original Sequence Size = "+originalSamples.length);
        System.out.println("Elongated Sequence Size = "+elongatedSequenceSize);

        b = new double[elongatedSequenceSize];
        smooth_b = new double[elongatedSequenceSize];

        for (int i = 0;( i / interpolateFactor + 1)<originalSamples.length; i++) {
            b[i] = Math.toIntExact(Math.round(originalSamples[i / interpolateFactor] + (1.0 * (i % interpolateFactor) / interpolateFactor) * (originalSamples[i / interpolateFactor + 1] - originalSamples[i / interpolateFactor])));
        }


        /**System.out.println("Interpolated Sequence:");
         for(i = 0;i<512;i++)
         {
         System.out.println(b[i]);
         }*/
        double value = b[0];
        Scanner in2 = new Scanner(System.in);
        System.out.println("enter smoothing coefficient: ");
        smoothing_coefficient = in2.nextDouble();

        //System.out.println("Original Sequence\tInterpolated Sequence\tSmoothed Interpolated Sequence(Coefficient = "+smoothing_coefficient+")");
        for (int i = 1; i < b.length; ++i) {
            double currentvalue = b[i];
            value += Math.toIntExact(Math.round((currentvalue - value) / smoothing_coefficient));
            smooth_b[i] = value;
        }

        System.out.println();
        System.out.println("elongated sequence: ");
        for(int i = 0; i < elongatedSequenceSize; i++){
            System.out.println((int)smooth_b[i]);
        }
    }

    void fft(){
        int n = originalSamples.length;
        int fft_size[] = new int[500];
        int x = 0;
        if(n != (Math.log(n)/Math.log(2))){
            for(int j = 0;j == (Math.log(j)/Math.log(2)) ; j++){
                if(j < n)fft_size[j] = originalSamples[j];
                else fft_size[j] = 0;
            }
        }
        else for(int j = 0; j < n; j++)fft_size[j] = originalSamples[j];

        int fft_even[] = new int[fft_size.length/2];
        int fft_odd[] = new int[fft_size.length/2];

        for(int i = 0; true; i++){
            if(i % 2 == 0)fft_even[i] = originalSamples[2 * i];
            else fft_odd[i] = originalSamples[2 * i + 1];
        }
    }
}
