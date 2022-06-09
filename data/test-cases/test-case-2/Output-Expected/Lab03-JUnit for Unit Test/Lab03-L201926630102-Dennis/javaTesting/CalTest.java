import org.junit.Before;
import org.junit.Test;

import java.util.concurrent.TimeoutException;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertEquals;

public class CalTest {
    Cal cal;

    @Before
    public void test(){
        cal = new Cal();
        assertNotNull(cal);
    }

    @Test
    public void testAdd() throws Exception {
        int sum = cal.add(1,2);
        assertEquals(3,sum);

        if (sum !=3)
            throw new Exception("Cal.add() has error result for input 1 and 2");

        assertEquals(5,cal.add(3,2));
    }

    @Test(expected = TimeoutException.class,timeout = 1000)
    public void testTimeOut(){
        cal.squareRoot(3);
    }

    @Test(expected = ArithmeticException.class)
    public void testException(){
        cal.divide(3,0);
    }
}
