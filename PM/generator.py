from numpy import random

NUMBER_OF_PATTERNS = 10

GENETIC_CODE_LENGTH = NUMBER_OF_PATTERNS

GENERATION_SIZE = 8

NEW_GENOMES_PER_GENERATION = 2

TOP_PARENTS_PER_GENERATION = 2


def generate_generation(parent_genomes, parent_weights=[], generation_size=GENERATION_SIZE, new_genomes=NEW_GENOMES_PER_GENERATION, top_parents=TOP_PARENTS_PER_GENERATION, **kwargs):

    generation = [generate_new_genome() for i in range(new_genomes)]

    if top_parents > 0 and len(parent_weights) > 0:
        zipped_parents = zip(parent_weights, parent_genomes)
        zipped_parents.sort()

        top_parents = zip(*(zipped_parents[:top_parents]))[1]
        generation.extend(top_parents)

    remaining_genomes = generation_size - len(generation)

    for i in range(remaining_genomes):
        generation.append(generate_genome(
            parent_genomes=parent_genomes, parent_weights=parent_weights, **kwargs))

    return generation


def generate_genome(parent_genomes, parent_weights=[], **kwargs):

    if len(parent_weights) == 0:
        parent_weights = [1.0/len(parent_genomes)] * len(parent_genomes)
    elif sum(parent_weights) != 1.0:
        divisor = sum(parent_weights) * 1.0
        parent_weights = map(lambda x: x / divisor, parent_weights)

    genome = [random.choice(map(lambda x: x[i], parent_genomes), p=parent_weights)
              for i in range(len(parent_genomes[0]))]

    mutate_genome(genome, **kwargs)

    return genome


def mutate_genome(genome, mutation_frequency=0.2, mutation_factor=0.2):

    for index, gene in enumerate(genome):
        if random.random() <= mutation_frequency:
            new_gene = int(gene * (1 + random.choice([1, -1])*mutation_factor))

            if new_gene < 0:
                new_gene = 0
            elif new_gene > 255:
                new_gene = 255

            genome[index] = new_gene

    return genome


def generate_new_genome(genetic_code_length=GENETIC_CODE_LENGTH):
    return [random.randint(0, 255) for i in range(genetic_code_length)]


def generate_pattern(genome, name="unnamed"):
    return
