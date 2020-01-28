import java.util.Scanner;

public class MCJ {
    public static void main(String[] args) {
        MCJ a = new MCJ();
        a.Dxy();
    }

    void Dxy(){
        int[] x = new int[128];
        int[] y = new int[128];
        int m = x.length, n = y.length;
        System.out.println("enter the time series:");
        Scanner scan = new Scanner(System.in);
        for(int i = 0; i < m; i++) x[i] = scan.nextInt();
        for(int i = 0; i < n; i++) y[i] = scan.nextInt();
        int tx, ty;
        double dxy = 0, dyx = 0;
        for(tx = 0, ty = 0; tx < m && ty < n; tx++){
            if (tx >= m || ty >= n) break;
            double costxy[] = minimumCost(x, tx, y, ty, m, n);
            dxy += costxy[0];
            /*double costyx[] = minimumCost(y, ty, x, tx, n, m);
            dyx = costyx[0];*/
            double[] delmin = minimumCost(x, tx, y, ty, m, n);
            ty += delmin[1] + 1;
        }
        System.out.println();
        System.out.println("x to y:");
        System.out.println(dxy);
        System.out.println();
        //System.out.println("y to x:");
        //System.out.println(dyx);

    }

    double[] minimumCost(int[] x, int tx, int[]y, int ty, int m, int n){
        double cmin = Double.POSITIVE_INFINITY;
        int del =0, delmin = 0;
        double temp;
        while (true){
            temp = Math.random();
            if (temp >= 0 || temp <= 100) break;
        }
        double beta = 1000;
        double phi = beta * ((4 * SD(y)) / Math.min(m, n));
       // double c = 0;
        while(ty + del < n){
            if (tx >= m) break;
            double c = Math.pow(phi * del, 2);
            //double c = 0;
            if(c >= cmin){
                if (ty + del > tx) break;
            }
            else{
               try {
                   c += Math.pow((x[tx] - y[ty + del]), 2);
                   if (c < cmin) {
                       cmin = c;
                       //System.out.println("local minimum cost:");
                       System.out.println(Math.round(cmin));
                       delmin = del;
                   }
               }
               catch(ArrayIndexOutOfBoundsException e)
               {
                   System.out.println("tx = "+tx+"\nty = "+ty+"\ndel = "+del);
               }
            }
            del++;
        }
        double returnStorage[] = new double[]{cmin, delmin};
        return returnStorage;

    }


   double SD(int[] arr){
        int  n = arr.length;
        int buff = 0;
        for(int i = 0; i < n; i++){
            buff += arr[i];
        }
        double avg = buff / n;
        double capSigma = 0;
        for (int i = 0; i < n; i++){
            capSigma += Math.pow((arr[i] - avg), 2);
        }
        return Math.sqrt(capSigma / n);
    }
}
