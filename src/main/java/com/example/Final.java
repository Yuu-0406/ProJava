public class Final {
    public static void main(String[] args) {
        final int CONST;
        CONST = 10;
        CONST = 20;
        method(CONST);
    }

    static void method(final int ARG) {
        System.out.println(ARG);
        ARG = 30;
        System.out.println(ARG);
    }
}
//エラーの例のプログラム