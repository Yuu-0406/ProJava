public class IntListWithBottom extends IntList{
    IntNode bottom;

    IntListWithBottom(){
        super();
        bottom = top;
    }

    @Override
    void addFirst(int val){
        if (top == null){
            top = bottom = new IntNode(val, null);
        } else {
            top = new IntNode(val, top);
        }
    }

    @Override
    int getLast(){
        if (bottom == null){
            return Integer.MIN_VALUE;
        } else{
            return bottom.val;
        }
    }

    @Override
    void addLast(int val){
        if (top == null){
            top = bottom = new IntNode(val, null);
        } else {
            bottom.next = new IntNode(val, null);
            bottom = bottom.next;
        }
    }

    public static void main(String[] args) {
        IntList list = new IntListWithBottom();
        list.addFirst(3);
        list.addFirst(5);
        list.addFirst(2);
        list.display();

        System.out.println();
        System.out.println("getFirst : " + list.getFirst());
        System.out.println("getLast   : " + list.getLast());

        System.out.println();
        list.addLast(9);
        System.out.println("getlast : " + list.getLast());

        System.out.println();
        list.display();
    }
}