//多次元配列と入れ子構造になったfor文
public class NestedStatement {
    public static void main(String[] args) {
        int[][] matrix = {{1,2,3},{10,20,30}};

        for (int i =0; i < 2; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.println(matrix[i][j]);
            }
        }

        for (int[] array : matrix) {
            for (int element : array) {
                System.out.println(element);
            }
        }
    }
}