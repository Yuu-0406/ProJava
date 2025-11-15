/* 整数のリンクリスト */
public class IntList{
    IntNode top;

    IntList(){
        top = null;
    }

    void addFirst(int val){
        top = new IntNode(val, top);
    }

    void display(){
        IntNode link = top;
        while (link != null){
            System.out.println(link.val);
            link = link.next;
        }
    }

    /*--- 第5回　練習問題　実装例 ---*/
    int getFirst(){
        if (top == null){
            return Integer.MIN_VALUE;
        } else {
            return top.val;
        }
    }

    int getLast(){
        if (top == null){
            return Integer.MIN_VALUE;
        }

        IntNode bottom = null;
        for (IntNode link = top; link != null; link = link.next){
            bottom = link;
        }

        return bottom.val;
    }

    void addLast(int val){
        IntNode newLink = new IntNode(val, null);

        if (top == null){
            top = newLink;
        } else {
            IntNode bottom = null;
            for (IntNode link = top; link != null; link = link.next){
                bottom = link;
            }
            bottom.next = newLink;
        }
    }

    public static void main(String[] args) {
        IntList list = new IntList();
        list.addFirst(3);
        list.addFirst(5);
        list.addFirst(2);
        list.display();
        

        /* 以下、第05回　練習問題確認用 */
        System.out.println("getFirst : " + list.getFirst());
        System.out.println("getLast  : " + list.getLast());
        list.addLast(9);
        list.display();
    }
}

// publicでないクラスならば、
//他のクラスのソースファイルに記述可能
class IntNode{
    int val;
    IntNode next;

    IntNode(int val, IntNode link){
        this.val = val;
        next = link;
    }
}