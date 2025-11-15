public class MatrixProduct{
    public static void main(String[] args){
        double[][] matrixA = {{1.1, 2.2, 3.3},{4.4, 5.5, 6.6}};
        double[][] matrixB = new double[3][2];
        matrixB[0][0] = 0.1; matrixB[0][1] = 0.4;
        matrixB[1][0] = 0.2; matrixB[1][1] = 0.5;
        matrixB[2][0] = 0.3; matrixB[2][1] = 0.6;

        double[][] ansMatrix = new double[2][2];
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                ansMatrix[i][j]  = 0.0;
                for (int k = 0; k < 3; k++) {
                    ansMatrix[i][j] = ansMatrix[i][j] + (matrixA[i][k] * matrixB[k][j]);
                }
            }
        }
        for (double[] row : ansMatrix){
            for (double element : row){
                System.out.print(element);
                System.out.print("\t");
            }
            System.out.println();
        }
    }
}