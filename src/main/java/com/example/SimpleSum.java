public class SimpleSum {
    public static void main(String[] args) {
        System.out.println(sum(10));
    }

    static int sum(int n) {
        int ans = 0;
        for (int i = 1; i <= n; i++) {
            ans = ans + i;
        }
        return ans;
    }
}