from .file import FileComponent, FileMetadataComponent
from .files_field import FilesFieldModelComponent
from .files_tests import FilesModelTestComponent
from .parent_record import ParentRecordComponent

file_components = [FileComponent, FileMetadataComponent, ParentRecordComponent, FilesFieldModelComponent,
                   FilesModelTestComponent]
