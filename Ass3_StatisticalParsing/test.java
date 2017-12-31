import edu.stanford.nlp.parser.nndep.DependencyParser;
import java.util.Properties;
import java.io.File;
import java.io.FileWriter;
import java.util.Scanner;
import java.io.*;
/**
 * Created by abhisheksinha on 3/20/17.
 */
public class test {
    public static void main(String[] args) {
        
        String testPath = args[2] + "/" + args[2] + "_test.conllx";    
        String seedmodelPath = "seed_models/" + args[0] + "_" + args[1];
        String testAnnotationsPath = "test_annotations/" + args[0] + "_" + args[1] + "_" + args[2] + "_test.conllx";

        DependencyParser model = DependencyParser.loadFromModelFile(seedmodelPath);		
        model.testCoNLL(testPath, testAnnotationsPath);		
    }
}
