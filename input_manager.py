import turtle
from time_manager import TimeStep
from bodies.planet import Planet
from bodies.star import Star
from physics_manager import PhysicsManager

bodies = []

#Funzione per chiedere la massa che dev'essere compresa fra 1 e 15 (*10^23kg)
def get_mass():
    
    while True:
        try:
            mass = float(input("Enter the mass of the body in the range [1;15]: "))
            if 1 <= mass <= 15:
               return mass
            
            else:
               print("Mass must be between 1 and 15.")

        except ValueError:
            print("Invalid input for mass. Please enter a number.")



#Funzione che chiede le coordinate della posizione del corpo
def get_position():

    while True:
        pos = input("Enter the posx, posy, comma-separated, within the range -400 to 400: ").strip()

        if ',' not in pos:
            print("Error! Please include a comma ('100,200').")
            continue
        
        try:
            posx, posy = map(float, pos.split(","))
            
            if -400 <= posx <= 400 and -400 <= posy <= 400:
                return posx, posy
            
            else:
                print("Position values must be between -300 and 300.")

        except ValueError:
            print("Error! Make sure you entered two valid numbers separated by a comma ('100,200').")



#Funzione che chiede le componenti della velocità del corpo

def get_vel():

    while True:
        vel = input("Enter the vx, vy comma-separated, within the range -2000 to 2000: ").strip()

        if ',' not in vel:
            print("Error! Please include a comma ('10,20').")
            continue
        
        try:
            vx, vy = map(float, vel.split(","))

            if -2000 <= vx <= 2000 and -2000 <= vy <= 2000:
               return vx, vy
            
            else:
               print("Velocity values must be between -2000 and 2000.")

        except ValueError:
               print("Error! Make sure you entered two valid numbers separated by a comma ('100,200').")



#Funzione principale per creare il corpo celeste :D 

def add_body():
    
    while True:
        answer = input("\nDo you want to add a body to the simulation? ").strip().lower()
        
        if answer == 'no':
           break  

        body_type = input("Enter the type of body (Planet/Star): ").strip().capitalize()

        if body_type not in ['Planet', 'Star']:
            print("Invalid type. Please choose 'Planet' or 'Star'.")
            continue

        try:
            mass = get_mass()
            posx, posy = get_position()
            vx, vy = get_vel()

            if body_type == "Planet":
               body = Planet(mass, posx, posy, vx, vy)

            elif body_type == "Star":
               body = Star(mass, posx, posy, vx, vy)

            bodies.append(body)

            print(f"{body_type} added successfully!")

        except ValueError:
            print("Invalid values entered. Please enter numbers for mass, position, and velocity.")
    
    print(f"Bodies in simulation: {len(bodies)}") 
    return bodies

#Funzione per stabilire la velocità della simulazione, se ci sono corpi inseriti
def get_simulation_speed(timeStep):
    
    if bodies == [] :
       print("No bodies were added")
       add_body()

    else:

        while True:

            try:
                speed = input("Enter the simulation speed ('0.1x', '1x', '10x'): ").strip()
            
                #NOTA!speed[:-1] per prendere tutta la stringa, tranne l'ultimo carattere

                if speed.endswith('x') and float(speed[:-1]) > 0: #se la stringa termina con x, 
                                                              #e se il numero float inserito è maggiore di 0,
                                                              #allora esegui:

                    timeStep.setTempo(speed)
                    break

                else:
                    print("Invalid format.")

            except ValueError:
                print("Invalid input.")


