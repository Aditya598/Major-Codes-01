// A learning vector quantization implementation in Java. 
// Input feature vectors are the DTW output costs which then 
// need to be classified 

import com.sun.javaws.IconUtil;
import sun.java2d.windows.GDIWindowSurfaceData;

import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class LVQ {

    public static void main(String[] args) {
        LVQ a = new LVQ();
        a.prepare_matrix();
    }

    static int[] uniform_distribution(int min, int max) {
        Integer[] arr = new Integer[max - min];
        for (int i = min; i < max; i++) arr[i] = i;
        Collections.shuffle(Arrays.asList(arr));
        int[] arr2 = new int[arr.length];
        for (int i = 0; i < arr2.length; i++) arr2[i] = (int) arr[i];
        return arr2;
        //return ThreadLocalRandom.current().nextInt(min, max + 1);
    }

    void prepare_matrix() {
        Scanner scan = new Scanner(System.in);
        int sum = 0, k = 0;
        System.out.println("prolonged data: ");
        int pb = scan.nextInt();
        sum += pb;
        System.out.println("right data: ");
        int r = scan.nextInt();
        sum += r;
        System.out.println("left data: ");
        int l = scan.nextInt();
        sum += l;
        System.out.println("number of  instances:");
        int instances = scan.nextInt();

        int[] targets = new int[sum];
        double[][] input = new double[sum][instances];

        System.out.println("enter data for target " + k);
        for (int i = 0; i < pb; i++) {
            targets[i] = k;
            for (int j = 0; j < instances; j++) {
                input[i][j] = scan.nextDouble();
            }
        }
        System.out.println("enter data for target " + ++k);
        for (int i = pb; i < pb + r; i++) {
            targets[i] = k;
            for (int j = 0; j < instances; j++) {
                input[i][j] = scan.nextDouble();
            }
        }
        System.out.println("enter data for target " + ++k);
        for (int i = pb + r; i < pb + r + l; i++) {
            targets[i] = k;
            for (int j = 0; j < instances; j++) {
                input[i][j] = scan.nextDouble();
            }
        }

        for (int i = 0; i < sum; i++) {
            for (int j = 0; j < instances; j++) {
                System.out.print(input[i][j] + "\t");
            }
            System.out.print("\t\t" + targets[i]);
            System.out.println();
        }

        Distance(input, targets, instances, sum);
    }

    static void Distance(double[][] input, int[] targets, int instances, int sum) {
        double[][] weights = new double[3][instances];
        int[] randBufBuf = new int[weights.length];
        System.out.println();
        System.out.println("weights:");
        int[] randBuf = uniform_distribution(0, sum);
        for (int i = 0; i < weights.length; i++) {
            randBufBuf[i] = randBuf[i];
            for (int j = 0; j < weights[0].length; j++) {
                weights[i][j] = input[randBuf[i]][j];
                System.out.print(weights[i][j] + "\t");
            }
            System.out.print("\t\t" + targets[randBuf[i]]);
            System.out.println();
        }

        System.out.println();
        System.out.println("rows from input to be excluded:");
        for (int i = 0; i < randBufBuf.length; i++) System.out.print(randBufBuf[i] + "\t");
        System.out.println();
        System.out.println();

        int[][] distance = new int[input.length - randBufBuf.length][weights.length];
        int k, l = 0;
        int[] targetEnhanced = new int[distance.length];
        boolean breakFlag = false;
        Arrays.sort(randBufBuf);
        for (int i = 0; i < input.length; i++, breakFlag = false) {
            for (int x = 0; x < weights.length; ++x) {
                if (i == randBufBuf[x]) {
                    //System.out.print(i + "\t");
                    breakFlag = true;
                    break;
                }
            }
            if (!breakFlag) {
                for (k = 0; k < weights.length; k++) {
                    for (int j = 0; j < weights[0].length; j++) {
                        distance[l][k] += (int) Math.sqrt(Math.pow((weights[k][j] - input[i][j]), 2));
                    }
                    System.out.print(distance[l][k] + "\t");
                }
                targetEnhanced[l] = targets[i];
                System.out.print("\t\t" + targetEnhanced[l]);
                System.out.println();
                l++;
            }
        }

        /*System.out.println("\n");
        System.out.println("distances");
        for (int i = 0; i < distance.length; i++) {
            for (int j = 0; j < distance[i].length; j++){
                System.out.print(distance[i][j] + "\t");
            }
            System.out.println();
        }*/
        int epoch = 0;

        errorCorrection(weights, targetEnhanced, distance, input, randBufBuf, epoch);

    }

    static void errorCorrection(double[][] weights, int[] target, int[][] distance, double[][] input, int[] buf, int epoch) {
        double alpha = 0.1;
        boolean breakFlag = false;
        int k = 0, l = 0;
        System.out.println("\n");
        System.out.println("minimum array");
        int[] minRow = new int[distance.length];
        int[] minCol = new int[distance.length];
        int[] minArr = new int[distance.length];
        for (int i = 0; i < distance.length; i++) {
            minArr[i] = distance[i][0];
            for (int j = 0; j < distance[i].length; j++) {
                if (minArr[i] > distance[i][j]) {
                    minArr[i] = distance[i][j];
                    minRow[i] = i;
                    minCol[i] = j;
                }
            }
            System.out.println(minArr[i] + "\t" + minRow[i] + "\t" + minCol[i]);
        }

        System.out.println();
        System.out.println("new distances");
        for (int i = 0; i < input.length; i++, breakFlag = false) {
            for (int x = 0; x < weights.length; ++x) {
                if (i == buf[x]) {
                    //System.out.print(i + "\t");
                    breakFlag = true;
                    break;
                }
            }
            if (!breakFlag) {
                for (k = 0; k < weights.length; k++) {
                    for (int j = 0; j < weights[0].length; j++) {
                        distance[l][k] += (int) Math.sqrt(Math.pow((weights[k][j] - input[i][j]), 2));
                    }
                    System.out.print(distance[l][k] + "\t");
                }
                System.out.print("\t\t" + target[l]);
                System.out.println();
                l++;
            }
        }

        System.out.println();
        for (int i = 0; i < distance.length; i++) {
            if (minArr[i] >= target[i] || epoch == 20) {
                for (int j = 0; j < input[i].length; j++) {
                        weights[minCol[i]][j] = weights[minCol[i]][j] - (alpha * (input[minRow[i]][j] - weights[minCol[i]][j]));
                }
                epoch++;
                errorCorrection(weights, target, distance, input, buf, epoch);
            }

            if (minArr[i] <= target[i] || epoch == 20) {
                for (int j = 0; j < input[i].length; j++) {
                    weights[minCol[i]][j] = weights[minCol[i]][j] + (alpha * (input[minRow[i]][j] - weights[minCol[i]][j]));
                }
                epoch++;
                errorCorrection(weights, target, distance, input, buf, epoch);
            }
        }
        System.out.println();
        System.out.println("new weights:");
        for (int i = 0; i < weights.length; i++) {
            for (int j = 0; j < weights[i].length; j++) {
                System.out.print(weights[i][j] + "\t");
            }
            System.out.println();
        }


    }


}
