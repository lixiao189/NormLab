import org.junit.Test;

import static org.junit.Assert.assertNotNull;

public class CalTest {
    @Test
    public void test() {
        Cal cal = new Cal();
        assertNotNull(cal);
    }

   /*@Test
    public void testAdd() {
        Cal cal = new Cal();
        int sum = cal.add(1, 2);
        assertEquals(3, sum);

        if(sum != 3)
            throw new Exception("Cal.add() has error result for input 1 and 2");

        assertEquals(4, cal.add(2, 2));
    }*/

    @Test(timeout = 1000)
    public void testTimeout() {
        Cal cal = new Cal();
        cal.squareRoot(3);
    }

    @Test(expected = ArithmeticException.class)
    public void testException() {
        Cal cal = new Cal();
        cal.divide(3, 0);
    }
}
