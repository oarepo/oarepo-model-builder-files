from .file import FileComponent
from .files_field import FilesFieldModelComponent
from .files_model import FilesDefaultsModelComponent, FilesRecordMetadataModelComponent, FilesResourceModelComponent, \
    FilesRecordModelComponent, FilesServiceModelComponent
from .files_tests import FilesModelTestComponent
from .parent_record import ParentRecordComponent

file_components = [FileComponent, ParentRecordComponent, FilesFieldModelComponent,
                   FilesModelTestComponent,
                   FilesDefaultsModelComponent,
    FilesRecordModelComponent,
    FilesRecordMetadataModelComponent,
    FilesResourceModelComponent,
    FilesServiceModelComponent]
