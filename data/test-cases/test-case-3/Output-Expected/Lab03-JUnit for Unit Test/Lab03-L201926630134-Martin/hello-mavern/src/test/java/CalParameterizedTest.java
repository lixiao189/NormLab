
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;

import java.util.Arrays;
import java.util.Collection;

import static org.junit.Assert.assertEquals;

@RunWith(Parameterized.class)
public class CalParameterizedTest {
    @Parameterized.Parameters
    public static Collection<Object[]> data() {
        return Arrays.asList(new Object[][]{
                {0, 0, 0}, {1, 1, 2}, {2, 3, 4}, {3, 5, 8}
        });
    }

    private int in1, in2;
    private int expected;

    public CalParameterizedTest(int in1, int in2, int expected) {
        this.in1 = in1;
        this.in2 = in2;
        this.expected = expected;
    }

    @Test
    public void test() {
        assertEquals(expected, new Cal().add(in1, in2));
    }
}