import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class matrix {
    Scanner scan = new Scanner(System.in);

    public static void main(String[] args) {
        matrix a = new matrix();
        //a.fillMatrix();
        //a.improved();
        a.DDTW();
    }

    void DDTW(){
        List<Integer> X01 = new ArrayList<>();
        List<Integer> Y01 = new ArrayList<>();
        Scanner scan = new Scanner(System.in);
        System.out.println("enter first wave");
        while (true){
            int a = scan.nextInt();
            if (a == -1)break;
            X01.add(a);
        }
        System.out.println("enter second wave");
        while (true){
            int a = scan.nextInt();
            if (a == -1)break;
            Y01.add(a);
        }
        int[] X = new int[X01.size()];
        int[] Y = new int[Y01.size()];
        for(int i = 0; i < X01.size(); i++){
            X[i] = X01.get(i);
        }
        //System.out.println("enter second series");
        for(int i = 0; i < Y01.size(); i++){
            Y[i] = Y01.get(i);
        }
        System.out.println();
        System.out.println("Distance of derivatives: ");
        int DerDist[][] = new int[Y.length][X.length];
        for(int i = 0; i < Y.length; i++){
            for(int j = 0; j < X.length; j++){
                if((i == 0 && j == 0) || (i == 0 && j != 0) || (j == 0 && i != 0)) DerDist[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
                else if(i + 1 >= Y.length || j + 1 >= X.length) DerDist[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
                else {
                    double Dx = ((X[j] - X[j - 1]) + ((X[j + 1] - X[j - 1]) / 2.0)) / 2.0;
                    double Dy = ((Y[i] - Y[i - 1]) + ((Y[i + 1] - Y[i - 1]) / 2.0)) / 2.0;
                    DerDist[i][j] = (int) Math.pow((Dx - Dy), 2);
                }
                System.out.print(DerDist[i][j] + "\t");
            }
            System.out.println();
        }

//        System.out.println();
//        System.out.println("Distance of derivatives: ");
//        int DerDist[][] = new int[500][500];
//        for(int i = 0; i < Y.length; i++){
//            for(int j = 0; j < X.length; j++){
//                if((i == 0 && j == 0) || (i == 0 && j != 0) || (j == 0 && i != 0)) DerDist[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
//                else if(i + 1 >= Y.length || j + 1 >= X.length) DerDist[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
//                else {
//                    DerDist[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
//                }
//                System.out.print(DerDist[i][j] + "\t");
//            }
//            System.out.println();
//        }

        int DTW[][] = new int[500][500];
        System.out.println();
        System.out.println("accumulated distances:");

        for(int i = 0; i < Y.length; i++){
            for(int j = 0; j < X.length; j++){
                if(i == 0 && j == 0) DTW[i][j] = DerDist[i][j];
                else if(i == 0 && j != 0)DTW[i][j] = DerDist[i][j] + DTW[i][j - 1];
                else if(j == 0 && i != 0 )DTW[i][j] = DerDist[i][j] + DTW[i - 1][j];
               /* DTW[i][0] = inf;
                DTW[0][j] = inf;*/
                else DTW[i][j] = DerDist[i][j] + Math.min(Math.min(DTW[i - 1][j], DTW[i - 1][j - 1]), DTW[i][j - 1]);
                System.out.print(DTW[i][j] + "\t");
            }
           System.out.println();
        }


        List<String> path = new ArrayList<>();
        int cost = 0;
        int i = Y.length - 1;
        int j = X.length - 1;
        System.out.println("warping path:");
        while (i > 0 && j > 0){
            int k = 0, l= 0;
            if (i == 0) j = j - 1;
            else if (j == 0) i = i - 1;
            else {
                if (DTW[i - 1][j] == Math.min(Math.min(DTW[i-1][j-1], DTW[i-1][j]), DTW[i][j-1])) i = i - 1;
                else if (DTW[i][j-1] == Math.min(Math.min(DTW[i-1][j-1], DTW[i-1][j]), DTW[i][j-1])) j = j - 1;
                else {
                    i = i - 1;
                    j = j - 1;
                }
            }
            System.out.println(DerDist[j][i]);
            try{
                cost += DerDist[j][i];
            }
            catch(ArrayIndexOutOfBoundsException e1)
            {
                System.out.println("Error: i = "+i+"\tj = "+j);
                System.out.println("rows = "+DerDist.length+"\tcolumns = "+DerDist[i].length);
            }
            path.add(j + "\t" + i);
        }
        path.add(0 + "\t" + 0);
        String path01[] = new String[path.size()];
        path.toArray(path01);
        System.out.println();
        System.out.println("optimal path: ");
        for (int l = 0; l < path01.length; l++) System.out.println(path01[l]);

        System.out.println();
        System.out.println("cost: ");
        System.out.println(cost / 100000.0);

    }

    void fillMatrix(){
        int[] X = new int[128];
        int[] Y = new int[128];
        Scanner scan = new Scanner(System.in);
        System.out.println("enter data");
        for(int i = 0; i < 128; i++){
            X[i] = scan.nextInt();
        }
        //System.out.println("enter second series");
        for(int i = 0; i < 128; i++){
            Y[i] = scan.nextInt();
        }
        System.out.println();
        System.out.println("Euclidean Distance between waves:");
        int EucDist[][] = new int[Y.length][X.length];
        for(int i = 0; i < Y.length; i++){
            for(int j = 0; j < X.length; j++){
                EucDist[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
                System.out.print(EucDist[i][j] + "\t");
            }
            System.out.println();
        }

        int DTW[][] = new int[Y.length][X.length];
        System.out.println();
        System.out.println("accumulated distances:");

        for(int i = 0; i < Y.length; i++){
            for(int j = 0; j < X.length; j++){
               if(i == 0 && j == 0) DTW[i][j] = EucDist[i][j];
                else if(i == 0 && j != 0)DTW[i][j] = EucDist[i][j] + DTW[i][j - 1];
                else if(j == 0 && i != 0 )DTW[i][j] = EucDist[i][j] + DTW[i - 1][j];
               /* DTW[i][0] = inf;
                DTW[0][j] = inf;*/
                else DTW[i][j] = EucDist[i][j] + Math.min(Math.min(DTW[i - 1][j], DTW[i - 1][j - 1]), DTW[i][j - 1]);
                System.out.print(DTW[i][j] + "\t");
            }
            System.out.println();
        }


        List<String> path = new ArrayList<>();
        int cost = 0;
        int i = Y.length - 1;
        int j = X.length - 1;
        while (i > 0 && j > 0){
            int k = 0, l= 0;
            if (i == 0) j = j - 1;
            else if (j == 0) i = i - 1;
            else {
                if (DTW[i - 1][j] == Math.min(Math.min(DTW[i-1][j-1], DTW[i-1][j]), DTW[i][j-1])) i = i - 1;
                else if (DTW[i][j-1] == Math.min(Math.min(DTW[i-1][j-1], DTW[i-1][j]), DTW[i][j-1])) j = j - 1;
                else {
                    i = i - 1;
                    j = j - 1;
                }
            }
            cost += EucDist[j][i];
            path.add(j + "\t" + i);
        }
        path.add(0 + "\t" + 0);
        String path01[] = new String[path.size()];
        path.toArray(path01);
        System.out.println();
        System.out.println("optimal path: ");
        for (int l = 0; l < path01.length; l++) System.out.println(path01[l]);

        System.out.println();
        System.out.println("cost: ");
        System.out.println(cost);

    }

    void improved(){
        int[] X = new int[128];
        int[] Y = new int[128];
        double inf = Double.POSITIVE_INFINITY;
        Scanner scan = new Scanner(System.in);
        System.out.println("enter first series");
        for(int i = 0; i < 128; i++){
            X[i] = scan.nextInt();
        }
        for(int i = 0; i < 128; i++){
            Y[i] = scan.nextInt();
        }
        int m = X.length, n = Y.length;
        double warpingDistance = 0.0;
        int distance[][] = new int[n][m];
        int cumulativeDistance[][] = new int[n][m];

        /**for Omega_1**/
        for(int i = 0; i < (2 * n - m)/3; i++){
            for(int j = 0; j < 2 * (2 * n - m)/3; j++ ){
                distance[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
            }
        }

        /**for Omega_2**/
        for(int i = (2 * n - m)/3; i < 2 * (2 * n - m)/3; i++){
            for(int j = (2 * n - m)/6; j < (4 * n - m)/6; j++ ){
                distance[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
            }
        }

        /**for Omega_3**/
        for(int i = (2 * m - n)/3; i < n; i++){
            for(int j = (2 * m - n)/3; j < m; j++ ){
                distance[i][j] = (int)Math.pow((X[j] - Y[i]), 2);
            }
        }

        for(int i = 0; i < distance.length; i++){
            for(int j = 0; j < distance[i].length; j++ ){
                System.out.print(distance[i][j] + "\t");
            }
            System.out.println();
        }
        System.out.println("\n");

        int[][] mirror = new int[distance.length][distance[0].length];
        for (int row = 0; row < distance.length; row++){
            int imageColumn = 0;
            for (int column = distance[row].length - 1; column >= 0; column--){
                int element = distance[row][column];
                mirror[row][imageColumn] = element;
                imageColumn++;
            }
        }
        for(int i = 0; i < mirror.length; i++){
            for(int j = 0; j < mirror[i].length; j++ ){
                System.out.print(mirror[i][j] + "\t");
            }
            System.out.println();
        }

        for(int i = 0; i < n; i++ ){
            for(int j = 0; j < m; j++){
                if(distance[i][j] == 0) continue;
                if(i == 0 && j == 0) cumulativeDistance[i][j] = distance[i][j];
                else if(i == 0 && j != 0)cumulativeDistance[i][j] = distance[i][0] + cumulativeDistance[i][j - 1];
                else if(j == 0 && i != 0 )cumulativeDistance[i][j] = distance[0][j] + cumulativeDistance[i - 1][j];
                /*cumulativeDistance[i][0] = (int)inf;
                cumulativeDistance[0][j] = (int)inf;*/
                else {
                    warpingDistance = Math.min(Math.min(cumulativeDistance[i - 1][j], cumulativeDistance[i - 1][j - 1]), cumulativeDistance[i][j - 1]);
                    warpingDistance += distance[i][j];
                }
                cumulativeDistance[i][j] = (int)warpingDistance;
            }
        }

        System.out.println("warping distance: ");
        System.out.println(warpingDistance);

        /** for(int i = 0; i < cumulativeDistance.length; i++){
         for(int j = 0; j < cumulativeDistance[i].length; j++ ){
         System.out.print(cumulativeDistance[i][j] + "\t");
         }
         System.out.println();
         }
         */
    }
}