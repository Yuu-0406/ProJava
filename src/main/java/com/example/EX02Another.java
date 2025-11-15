/*第二回練習問題　実装例 */
public class EX02Another{
    public static void main(String[] args) {
        int[] array = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        int sum =0;

        for (int element : array) {
            sum = sum + element;
        }

        System.out.println(sum);
    }
}