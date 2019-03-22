####################################################
#
#   Cambia Bowling Test
#
#   Grayson Taylor
#
#   The goal is to:
#   Create a 10-pin bowling scoring application
#   that uses traditional scoring rules to score each frame.
#
#
####################################################

import sys




'''
Print the score
'''
def print_score(frame, score):
    print("Frame: " + str(frame) + " Current Score: " + str(score))


'''
Parse the user input, and do some validation checking
The parsed input will be converted to integers
-2 is a strike
-1 is a spare
Note:
I don't believe I have handled all invalid entries
especially for the last frame
validation can probably be optimized
'''
def parse_and_validate(input_score, frame):
    parsed = input_score.split(',')
    output = []
    # Handle no entry or a strike being the first value in a frame
    if len(parsed) == 0 or parsed[0] == '/' or len(parsed) > 3:
        return None
    
    # Loop through each bowl in the frame.
    prev_val = ''
    for val in parsed:
        val = val.strip()
        if val == 'X' or val == 'x': # Handle a strike
            if len(parsed) == 1 or frame == 9: # Only want one strike unless last frame
                output.append(-2) # save the ouput as a -2 for strike
            else:
                return None
        elif val == '/':
            if len(parsed) > 1: # You can't have a frame with only a spare
                # Check if the previous bowl was spare or strike
                if prev_val == 'X' or prev_val == 'x' or prev_val == '/':
                    return None
                output.append(-1) # Add the spare as -1
            else:
                return None
        else:
            try: # Try/Catch just in case an exception happens when converting to int
                # Avoid inputted values less than 0 or greater than 10
                if int(val) >= 0 and int(val) < 10:
                    output.append(int(val))
                else:
                    return None
            except:
                return None
        prev_val = val
            
    # We don't want a sum greater than 10 for a frame with 2 entries
    if sum(output) > 10 and len(output) < 3:
        return None
    
    return output

'''
Handles any unresolved strikes or spares that have previously appeared
Adds in the values from the new frames
'''
def handle_unresolved(unres_q, frame_values):
    for i in range(0, len(unres_q)): # Loop through the unresolved frames
        bowl_num = 0
        unresolved = unres_q[i]
        for j in range(0, len(unresolved)): # Loop through the values in the unresolved frame
            val = unresolved[j]
            # The goal is to replace negative values with values to add in
            if val < 0 and bowl_num < len(frame_values):
                num_to_add = frame_values[bowl_num]
                bowl_num = bowl_num + 1
                
                if num_to_add < 0:
                    # If the number we are adding in is spare or strike
                    if num_to_add == -1:
                        # We want the value of the bowl not the 10 as a spare
                        unres_q[i][j] = 10 - frame_values[0]
                    else:
                        unres_q[i][j] = 10 
                else:
                    unres_q[i][j] = num_to_add # Otherwise add in its value
      
    return unres_q

'''
Handle the last frame, this method is mainly useful for handling ending strikes/spares
'''
def resolve_last_frame(frame_scores):
    # If all the values in the frame are numbers just sum and return
    if all(i > 0 for i in frame_scores):
        return sum(frame_scores)

    final_frame_score = 0
    # Loop throug the final frame
    for i in range(0, len(frame_scores)):
        val = frame_scores[i]
        if val == -2: # If we get a strike, handle the next two values
            final_frame_score = final_frame_score + 10 # Add 10 for strike
            
            if frame_scores[i+1] < 0:
                final_frame_score = final_frame_score + 10 # Add 10 for strike or spare
            else:
                final_frame_score = final_frame_score + frame_scores[i+1] # Add value

            if frame_scores[i+2] == -2:
                final_frame_score = final_frame_score + 10 # Add 10 for strike or spare
            elif frame_scores[i+2] == -1:
                final_frame_score = final_frame_score + 10 - frame_scores[i+1]
            else:
                final_frame_score = final_frame_score + frame_scores[i+2] # Add value
            break
        elif val == -1: # If we get a spare, handle next value
            final_frame_score = final_frame_score + 10

            if frame_scores[i+1] < 0: # Add 10 for strike
                final_frame_score = final_frame_score + 10
            else:
                final_frame_score = final_frame_score + frame_scores[i+1] # Add value
            break
            
    return final_frame_score

            

def main():
    # Output Instructions
    instructions = ("Input the score for each frame. "
                    "Possible scores are: \n"
                    " X - Strike \n"
                    " #,/ - Spare \n"
                    " #,# - ex: 2,3 \n"
                    " X,X,X or X,X,# or X,#,/ or #,/,# or #,/,X "
                    "- possible 3 attempts for 10th frame.\n"
                    "Numbers should be between 0 and 9.\n")
    print(instructions)

    total_score = 0
    unres_scores_q = [] # Unresolved score queue i.e. strikes and spares
    frame = 0
    while frame < 10:
        # Print frame and handle inputting the score
        print("Frame: " + str(frame + 1))
        input_score = input("Input Score: ")
        parsed_score = parse_and_validate(input_score, frame) # Parse Score into ints

        # Check if input was validated
        if not parsed_score or len(parsed_score) < 1:
            print("Invalid Input Try Again")
            continue
        # Handle any unresolved strikes or spares in the Queue
        if len(unres_scores_q) > 0:
            unres_scores_q = handle_unresolved(unres_scores_q, parsed_score) # Update scores
            while len(unres_scores_q) > 0: # Loop through the unhandle scores
                # If all of the values for the strike/spare are handled
                # pop it out of the queue and add it to the total
                if all(i >= 0 for i in unres_scores_q[0]):
                    unres = unres_scores_q.pop(0)
                    total_score = total_score + sum(unres)
                else:
                    break

        if frame == 9: # Handle the final frame
            try: # Try/Catch to handle any possible errors in last frame
                # Handle the score for the last frame
                total_score = total_score + resolve_last_frame(parsed_score)
                print_score(frame + 1, total_score) # Print it
            except:
                print("Error Occurred, please redo frame")
                continue
        elif -2 in parsed_score:
            # If strike, add to Queue (the -1 signify the next two bowls to be calculated)
            unres_scores_q.append([10,-1,-1])
            # frame 0 print blank else print score
            if frame == 0:
                print_score(frame + 1, "")
            else:
                print_score(frame + 1, total_score)
        elif -1 in parsed_score:
            # If spare, add to Queue (the -1 signify the next bowl to be calculated)
            unres_scores_q.append([10, -1])
            # frame 0 print blank else print score
            if frame == 0:
                print_score(frame + 1, "")
            else:
                print_score(frame + 1, total_score)
        else:
            # If a normal bowl sum it and print the score
            total_score = total_score + sum(parsed_score)
            print_score(frame + 1, total_score)

        frame = frame + 1 # increment frame
            



main() # RUN the program
 
    
