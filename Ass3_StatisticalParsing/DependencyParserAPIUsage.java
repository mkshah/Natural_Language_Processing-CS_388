import edu.stanford.nlp.parser.nndep.DependencyParser;
import java.util.Properties;
import java.io.File;
import java.io.FileWriter;
import java.util.Scanner;
import java.io.*;
/**
 * Created by abhisheksinha on 3/20/17.
 */
public class DependencyParserAPIUsage {
    public static void main(String[] args) {
        
		//  Training/Testing Data path
        String seedPath = args[0] + "/" + args[0] + "_train_" + args[1] + ".conllx";
		String selfTrainingPath = args[2] + "/" + args[2] + "_train_" + args[3] + ".conllx";
        String testPath = args[2] + "/" + args[2] + "_test.conllx";    
		
		// Path were combined (seed + selftrained) annotations will be present
		String fullTrainingPath = "full_training/" + args[0] + "_" + args[1] + "_" + args[2] + "_" + args[3] + ".conllx";
		
		// Path to embedding vectors file
        String embeddingPath = "en-cw.txt";
        
		// Path where model is to be saved
        String seedmodelPath = "seed_models/" + args[0] + "_" + args[1];
        String fullmodelPath = "full_models/" + args[0] + "_" + args[1] + "_" + args[2] + "_" + args[3] ;
		
		// Path where data annotations are stored
		String selfTrainingAnnotationsPath = "selfTraining_annotations/" + args[0] + "_" + args[1] + "_" + args[2] + "_" + args[3] + ".conllx";
        String testAnnotationsPath = "test_annotations/" + args[0] + "_" + args[1] + "_" + args[2] + "_" + args[3] + ".conllx";

        // Configuring propreties for the parser. A full list of properties can be found
        // here https://nlp.stanford.edu/software/nndep.shtml
        Properties prop = new Properties();
        prop.setProperty("maxIter", "200");
        DependencyParser p = new DependencyParser(prop);
		
        // Argument 1 - Training Path
        // Argument 2 - Dev Path (can be null)
        // Argument 3 - Path where model is saved
        // Argument 4 - Path to embedding vectors (can be null)
		// Training on Seed data
        p.train(seedPath, null, seedmodelPath, embeddingPath);		
        // Load a saved path
        DependencyParser model = DependencyParser.loadFromModelFile(seedmodelPath);		
        // Test model on Self training data
        model.testCoNLL(selfTrainingPath, selfTrainingAnnotationsPath);
		
		// Merging seed and selftraining data in a single file
		try
		{			
			File file1 = new File(seedPath);
			File file2 = new File(selfTrainingAnnotationsPath);
			File file3 = new File(fullTrainingPath);
			
			FileWriter fw = new FileWriter(file3);	
			Scanner sc1 = new Scanner(file1);
			Scanner sc2 = new Scanner(file2);
			
			while(sc1.hasNextLine()){
				fw.write(sc1.nextLine());
				fw.write("\n");
			}
			while(sc2.hasNextLine()){
				fw.write(sc2.nextLine());
				fw.write("\n");
			}
			fw.close();
		}
		catch(IOException e1)
		{		
			System.out.println(e1);
		}
		
		// Training on combined data
		p.train(fullTrainingPath, null, fullmodelPath, embeddingPath, seedmodelPath);
		// Loading final model
		DependencyParser model1 = DependencyParser.loadFromModelFile(fullmodelPath);
		// Testing 
		model1.testCoNLL(testPath, testAnnotationsPath);
    }
}
