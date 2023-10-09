import os
import json
from Extractors.extract import TextExtractor
from Extractors.scrapper import LinkScrapper
from Database.Vectorial.vector_database import FullControl


def get_directories(path):
    return [os.path.join(path, o) for o in os.listdir(path) if os.path.isdir(os.path.join(path, o))]


def get_files(path):
    return [os.path.join(path, o) for o in os.listdir(path) if os.path.isfile(os.path.join(path, o))]


all_files = []


def get_all_files(dir):
    files = get_files(dir)
    all_files.append(files)

    for dir in get_directories(dir):
        get_all_files(dir)


def split_text(text, desired_chunks=5, max_chunk_length=600):
    """
    A safer version of the function that avoids index out of range errors.
    """

    avg_chunk_length = len(text) // desired_chunks
    avg_chunk_length = min(avg_chunk_length, max_chunk_length)

    chunks = []
    start = 0
    end = avg_chunk_length

    while start < len(text):
        # Find the nearest end of sentence for slicing but ensure end doesn't exceed text length
        while end < len(text) and text[end] not in ['.', '!', '?', '\n']:
            end += 1
        end = min(end + 1, len(text))  # Include the punctuation or newline and ensure not exceeding text length

        # If chunk is too large, split it further but ensure mid doesn't exceed text length
        while end - start > max_chunk_length:
            mid = start + max_chunk_length
            while mid > start and mid < len(text) and text[mid] not in ['.', '!', '?', '\n']:
                mid -= 1
            mid = min(mid + 1, len(text))  # Include the punctuation or newline and ensure not exceeding text length
            chunks.append(text[start:mid].strip())
            start = mid

        chunks.append(text[start:end].strip())
        start = end
        end = start + avg_chunk_length

    # Remove any potential empty chunks
    chunks = [chunk for chunk in chunks if chunk]

    return chunks


def update_info(do_process=False):
    get_all_files('Files')
    with open(os.path.join('Files', 'properties.json'), 'r') as f:
        properties = json.load(f)

    vector_database = FullControl()
    new_file_info = {}
    for i in all_files:
        # Remove ignore.json and properties.json from list
        if os.path.join('Files', 'ignore.json') in i:
            i.remove(os.path.join('Files', 'ignore.json'))
        if os.path.join('Files', 'properties.json') in i:
            i.remove(os.path.join('Files', 'properties.json'))

        # Get the meta file of the folder if it exists
        meta = None
        for j in i:
            if j.endswith('meta.json'):
                with open(j, 'r') as f:
                    meta = json.load(f)
                i.remove(j)
                break

        for j in i:
            if j.endswith('links.txt'):
                with open(j, 'r') as f:
                    for line in f.readlines():
                        try:
                            scrapper = LinkScrapper(line.strip())
                            info = {
                                'content': scrapper.scrap_text(),
                                'metadata': meta
                            }
                            if line in properties:
                                if info != properties[line]:
                                    print(f'Link modified: {line}')
                                    if do_process:
                                        # Get the last chunks
                                        last_chunks = split_text(properties[line]['content'])

                                        # Delete the last chunks from the database
                                        for chunk in last_chunks:
                                            vector_database.delete(chunk)

                                        # Get the new chunks
                                        new_chunks = split_text(info['content'])

                                        # Insert the new chunks into the database
                                        for chunk in new_chunks:
                                            vector_database.insert(chunk, meta)
                            else:
                                print(f'Link added: {line}')
                                if do_process:
                                    # Get the new chunks
                                    new_chunks = split_text(info['content'])

                                    # Insert the new chunks into the database
                                    for chunk in new_chunks:
                                        vector_database.insert(chunk, meta)
                            new_file_info[line] = info
                        except:
                            print(f'Link failed: {line}')

            else:
                try:
                    extractor = TextExtractor(j)
                    info = {
                        'content': extractor.extract(),
                        'metadata': meta
                    }
                    if j in properties:
                        if info != properties[j]:
                            print(f'File modified: {j}')
                            if do_process:
                                # Get the last chunks
                                last_chunks = split_text(properties[j]['content'])

                                # Delete the last chunks from the database
                                for chunk in last_chunks:
                                    vector_database.delete(chunk)

                                # Get the new chunks
                                new_chunks = split_text(info['content'])

                                # Insert the new chunks into the database
                                for chunk in new_chunks:
                                    vector_database.insert(chunk, meta)
                    else:
                        print(f'File added: {j}')
                        if do_process:
                            # Get the new chunks
                            new_chunks = split_text(info['content'])

                            # Insert the new chunks into the database
                            for chunk in new_chunks:
                                vector_database.insert(chunk, meta)

                    new_file_info[j] = info
                except:
                    print(f'File failed: {j}')

    print('\n')
    for i in new_file_info.keys():
        print(f'File: {i} - {new_file_info[i]}')

    if do_process:
        with open(os.path.join('Files', 'properties.json'), 'w') as f:
            json.dump(new_file_info, f, indent=4)
