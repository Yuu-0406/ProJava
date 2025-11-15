/*第二回練習問題　実装例 */
public class EX02{
    public static void main(String[] args) {
        int[] array = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
        int sum =0;

        for(int i = 0; i < array.length; i++){
            sum = sum + array[i];
        }

        System.out.println(sum);
    }
}